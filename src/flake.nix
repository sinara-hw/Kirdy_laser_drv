{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";

  outputs = { self, nixpkgs }: {

    devShells.x86_64-linux.default =
      let pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in pkgs.mkShell {
        name = "kicad-dev-shell";
        buildInputs = [ pkgs.kicad ];
        shellHook = ''
          export KICAD7_3DMODEL_DIR=${pkgs.kicad.libraries.packages3d}
          export PYTHONPATH=${pkgs.kicad.base}/share/kicad/plugins
          export OUTPUT_DIR=$(pwd)/production
        '';
      };

    defaultPackage.x86_64-linux = # Notice the reference to nixpkgs here.
      with import nixpkgs { system = "x86_64-linux"; };
      stdenv.mkDerivation {
        name = "proj";
        src = self;

        nativeBuildInputs = [ pkgs.kicad pkgs.python3 ];
        buildPhase = ''
          export HOME=/tmp
          echo ${src}
          kicad-cli sch export pdf ${src}/kirdy.kicad_sch -o kirdy.pdf
        '';
        installPhase = "echo test";
      };

  };
  # pkgs = nixpkgs.legacyPackages.x86_64-linux;
  #       nativeBuildInputs = [
  #          pkgs.kicad pkgs.python3
  #       ];

}
