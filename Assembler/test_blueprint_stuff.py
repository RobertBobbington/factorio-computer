from blueprint_generator import Blueprint
import blueprint_import_export

import json

bp = Blueprint()

#bp.generate_rom_entities(4)

json_stf = json.dumps(bp.json_dict)


# create

compressed_bp = blueprint_import_export.bp_compress(json_stf)

done_bp = blueprint_import_export.bp_encode_base64(compressed_bp)

print(done_bp)

# import (to json)

#large_bp = ""

#print(blueprint_import_export.bp_decompress(blueprint_import_export.bp_decode_base64(large_bp)))

# decode and decompres single line PROM template
prom_template = "0eNqtlFFuozAQhu8yz1AllGxSpN5h31cVMjBNRwLbssdRUMUB9hb7shfbk3QMbYNK2myrvoAM83/4/2fMI1RtQOtIMxSP4LWyKZt076iJ6yMU6wR6uQ4JqMqbNjCmscqS3kPBLmACVBvtofgletpr1UYl9xahAGLsIAGturhqsKYGXVqbriKt2DgQLukGj+MnLgI0HQlTDpVsolNtO5Nnw10CqJmYcNrMuOhLHboK3WjkPUoC1ngRGv1senW1GW3LfYjbeoPKPoFaz1AJSFLsTFtW+KAOJP6lqCZXB+JS3jWvyntynssLcdTGWonTOISJ7VnFRqbZOt/mu+sf+S4+7qxyY9gF/Pv9F4Zzlq5n0Akz79LCVfZxQPlHLV/A8llADTmsp3fZ+bieiae4/Bfz8hgRS82BHAfVnmRTRfpzCnmW5q3UmMA28P9T8ICu54d4fEac7cVJ0FzeO9OVpAU2nauzbdqccHHc0lZ1dhno5ltn7kIeL0O3WozanzhqcirHJhSzP00CEoKfmryTUb3JZFp3N9l6OwxPg7yQMA=="
prom_template_decode = blueprint_import_export.bp_decode_base64(prom_template)
prom_template_decompressed = blueprint_import_export.bp_decompress(prom_template_decode)
print(prom_template_decompressed)
work_bp =dict()
work_bp["entities"] = json.loads(prom_template_decompressed)["blueprint"]["entities"]

with open("json_test.json", "w") as outfile:
    json.dump(work_bp, outfile, ensure_ascii=False, indent=4)
