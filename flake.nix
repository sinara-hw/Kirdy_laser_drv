{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
  inputs.kicad_bom_generator = {
    url = "git+https://git.m-labs.hk/linuswck/KiCAD_BOM_Generator.git";
    flake = false;
  };

  outputs = { self, nixpkgs, kicad_bom_generator }: {
    formatter.x86_64-linux = nixpkgs.legacyPackages.x86_64-linux.nixfmt;

    devShells.x86_64-linux.default =
      let pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in pkgs.mkShell {
        name = "kicad-dev-shell";
        buildInputs = [ pkgs.kicad ];
      };

    defaultPackage.x86_64-linux =
      with import nixpkgs { system = "x86_64-linux"; };
      stdenv.mkDerivation {
        name = "production_files";
        src = ./src;

        nativeBuildInputs = [ pkgs.kicad pkgs.zip pkgs.python3 ];

        buildPhase = ''
          # kicad-cli requires the use of $HOME
          export HOME=/tmp

          SCH=kirdy.kicad_sch
          PCB=kirdy.kicad_pcb

          # Get Revision Number from the Title Block in KiCAD Top Schematics
          REV=$(cat $SCH | grep rev | cut -d'"' -f 2)
          PREFIX=kirdy_$REV

          kicad-cli sch export python-bom $SCH -o $PREFIX"_bom".xml
          export PYTHONPATH=${pkgs.kicad.base}/share/kicad/plugins
          python ${kicad_bom_generator}/generate_bom_from_xml.py $PREFIX"_bom".xml $PREFIX"_bom".csv

          kicad-cli sch export pdf $SCH -o $PREFIX.pdf
          kicad-cli pcb export pos $PCB --format csv --units mm  -o $PREFIX"_pos".csv

          export KICAD7_3DMODEL_DIR=${pkgs.kicad.libraries.packages3d}/share/kicad/3dmodels
          kicad-cli pcb export step $PCB --subst-models --force -o $PREFIX.step

          mkdir -p $PREFIX"_gerber_drill"
          kicad-cli pcb export gerbers $PCB -l 'F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts' --no-x2 --subtract-soldermask -o ./$PREFIX"_gerber_drill"

          # The additional trailing slash is due to a bug in the kicad-cli tool. https://gitlab.com/kicad/code/kicad/-/issues/14438
          kicad-cli pcb export drill $PCB -u mm --generate-map --map-format gerberx2 -o ./$PREFIX"_gerber_drill"/

          zip -r -j $PREFIX"_gerber_drill" $PREFIX"_gerber_drill"
        '';

        installPhase = ''
          mkdir -p $out/production_files 
          cp $PREFIX"_bom".csv $out/production_files/$PREFIX"_bom".csv
          cp $PREFIX.pdf $out/production_files/$PREFIX.pdf
          cp $PREFIX"_pos".csv $out/production_files/$PREFIX"_pos.csv"
          cp $PREFIX.step $out/production_files/$PREFIX.step
          cp $PREFIX"_gerber_drill".zip $out/production_files/$PREFIX"_gerber_drill".zip
        '';
      };
  };
}
