from UI import *
from DB import *

if __name__ == "__main__":
    root = UIMain()
    dbClient = MongoDB()
    key_dict = dbClient.load_keys()
    root.keyBox["values"] = [key for key in key_dict.keys()]
    root.orgBox["values"] = [name for name in key_dict.values()]
    root.mainloop()
