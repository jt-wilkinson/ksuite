class KDocument:

    def __init__(self):

        self.objects = []
        self.stitches = []

    def add_object(self, obj):

        self.objects.append(obj)

    def clear(self):

        self.objects = []
        self.stitches = []

    def generate_stitches(self, generator):

        self.stitches = []

        for obj in self.objects:

            seq = generator(obj)

            self.stitches.append(seq)