import os

dir1 = "./production/svg"
dir2 = "./production/svg_org"

svg_sch_files = os.popen("ls ./production/svg").read().split("\n")
svg_org_sch_files = os.popen("ls ./production/svg_org").read().split("\n")

print(svg_sch_files)
print(svg_org_sch_files)
for org_svg in svg_org_sch_files:
    print("#############")
    #print(os.path.join('./production/svg', svg))
    print(os.path.join('./production/svg', org_svg))
    os.system(f"python -m scripts.k-eediff-svg {os.path.join('./production/svg', org_svg)} {os.path.join('./production/svg_org', org_svg)}")