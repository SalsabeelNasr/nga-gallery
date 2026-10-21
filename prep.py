import csv, json, sys, collections
csv.field_size_limit(10**9)
src = sys.argv[1]
objs = {}
with open(f"{src}/objects.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        objs[r["objectid"]] = r
rows = []
classes = collections.Counter()
with open(f"{src}/published_images.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["viewtype"] != "primary" or r["openaccess"] != "1": continue
        o = objs.get(r["depictstmsobjectid"])
        if not o: continue
        cls = o["classification"] or "Other"
        classes[cls] += 1
        try: by = int(o["beginyear"])
        except: by = None
        rows.append([r["uuid"], o["title"][:160], (o["attribution"] or "")[:100], o["displaydate"][:40], cls, by, int(r["width"] or 0), int(r["height"] or 0), int(o["objectid"])])
rows.sort(key=lambda x: (x[4] != "Painting", -(x[6]*x[7] > 0), x[8]))
print(len(rows), classes.most_common())
cls_list = sorted(classes, key=lambda c: -classes[c])
ci = {c:i for i,c in enumerate(cls_list)}
for r in rows: r[4] = ci[r[4]]
json.dump({"classes": cls_list, "rows": rows}, open("data.json","w"), ensure_ascii=False, separators=(",",":"))
