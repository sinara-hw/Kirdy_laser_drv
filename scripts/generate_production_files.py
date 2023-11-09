import os
import argparse

__cmd_get_kicad_bin_path = "which kicad | xargs readlink | sed 's/$/-cli/' | xargs readlink"

def setup_env(prefix, sch, out_dir, dir_kicad_plugins, dir_3d_models):
    # Get the path to "kicad_netlist_reader.py" script in NixOs
    if dir_kicad_plugins is None:
        dir_kicad_plugins = os.path.join(os.popen(__cmd_get_kicad_bin_path).read().replace("\n", ""),
            "../../share/kicad/plugins")
    
    # Setup the PYTHONPATH for "generate_bom_from_xml.py" to import "kicad_netlist_reader"
    try:
        pythonpath = os.environ['PYTHONPATH']
    except KeyError:
        pythonpath = ''
    pathlist = [dir_kicad_plugins]
    if pythonpath:
        pathlist.extend(pythonpath.split(os.pathsep))
    os.environ['PYTHONPATH'] = os.pathsep.join(pathlist)

    # NIXOS installs KiCAD Built-in 3D models in a separated folder
    if dir_3d_models is None:
        model_3d_path = os.path.join("/nix/store", os.popen("ls /nix/store | grep kicad-packages3d | head -1").read().replace("\n", ""), "share/kicad/3dmodels")
    # Setup the KICAD7_3DMODEL_DIR for step file to be generated with kicad-cli"
    os.environ['KICAD7_3DMODEL_DIR'] = model_3d_path

    # Generate the prefix from the title and revision fields in title block of the schematics top
    if prefix is None:
        with open (sch, "r") as f:
            data = f.read().splitlines()
            title_line = data[7][1:-1].split()
            revision_line = data[9][1:-1].split()
        if title_line[0].find("title") and revision_line[0].find("rev"):
            ret_prefix = f"{title_line[1][1:-1]}_{revision_line[1][1:-1]}"
        else:
            raise ValueError("Prefix cannot be generated from schematic file.")
    else:
        ret_prefix = prefix

    gerber_drill_dir = os.path.join(out_dir, f"{ret_prefix}_gerber_drill")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(gerber_drill_dir):
        os.makedirs(gerber_drill_dir)

    return ret_prefix

def generate_production_files(prefix, sch, pcb, out_dir):
    out_path = os.path.join(out_dir, prefix)

    bom_ret_code = os.system(f"kicad-cli sch export python-bom {sch} -o {out_path}_bom.xml")
    bom_ret_code |= os.system(f"python -m scripts.generate_bom_from_xml {out_path}_bom.xml  {out_path}_bom.csv")
    os.system(f"rm {out_path}_bom.xml")

    pdf_ret_code = os.system(f"kicad-cli sch export pdf {sch} -o {out_path}.pdf")

    pos_ret_code = os.system(f"kicad-cli pcb export pos {pcb} --format csv --units mm  -o {out_path}_pos.csv")

    step_ret_code = os.system(f"kicad-cli pcb export step {pcb} --subst-models --force -o {out_path}.step")

    out_path = os.path.join(out_dir, f"{prefix}_gerber_drill")
    
    gerber_ret_code = os.system(f"kicad-cli pcb export gerbers {pcb} -l 'F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts' --no-x2 --subtract-soldermask -o {out_path}")
    
    # The additional trailing slash is due to a bug in the kicad-cli tool. https://gitlab.com/kicad/code/kicad/-/issues/14438
    drill_ret_code = os.system(f"kicad-cli pcb export drill {pcb} -u mm --generate-map --map-format gerberx2 -o {out_path}/")
    zip_ret_code = os.system(f"zip -r -j {out_path} {out_path}")
    os.system(f"rm -r {out_path}")

    print("=== File Generation Status === ")
    print("Gerber: {}".format("Success" if gerber_ret_code == 0 else "Failed"))
    print("Drill: {}".format("Success" if drill_ret_code == 0 else "Failed"))
    print("Zip_Gerber_Drill: {}".format("Success" if zip_ret_code == 0 else "Failed"))
    print("Bom: {}".format("Success" if bom_ret_code == 0 else "Failed"))
    print("Pdf: {}".format("Success" if pdf_ret_code == 0 else "Failed"))
    print("Pos: {}".format("Success" if pos_ret_code == 0 else "Failed"))
    print("Step: {}".format("Success" if step_ret_code == 0 else "Failed"))

def main():
    parser = argparse.ArgumentParser(
        description="Python Script to Generate Production Files(Gerber, Drill, Drill Map, Bom, Component Placement, Schematics PDF, Step Files)")
    parser.add_argument("-s", "--sch",  
                        default="kirdy.kicad_sch",
                        help="schematics top file. defaults to 'kirdy.kicad_sch' if omitted")
    parser.add_argument("-p", "--pcb",  
                        default="kirdy.kicad_pcb",
                        help="pcb file. defaults to 'kirdy.kicad_pcb' if omitted")
    parser.add_argument("-o", "--output",  
                        default="./production",
                        help="output folder, defaults to './production' if omitted")
    parser.add_argument("-pre", "--prefix",  
                    default=None,
                    help="output filename prefix, attempts to generated from schematics top file if omitted")
    parser.add_argument("-dir_plugins", "--dir_kicad_plugins",  
                default=None,
                help="path to kicad_netlist_reader.py, attempts to find the required path in the system if omitted")
    parser.add_argument("-dir_3d", "--dir_3d_models",  
                default=None,
                help="path to kicad 3d models folder, attempts to find the required path in the system if omitted")

    args = parser.parse_args()

    prefix = setup_env(args.prefix, args.sch, args.output, args.dir_kicad_plugins, args.dir_3d_models)

    generate_production_files(prefix, args.sch, args.pcb, args.output)

if __name__ == '__main__':
    main()