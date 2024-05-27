from base.web import WebKeys


class Template(WebKeys):
    def run(self, key):
        print(f"Run Template: {key}")
