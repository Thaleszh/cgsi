class OBJDescriptor:

    def write_obj(self, obj_name, obj, path):
        description = 'o ' + obj_name + '\n'
        for vertice in obj.coordinates:
            description += 'v {} {} 0\n'.format(vertice[0], vertice[1])
        description = description[:-1]
        f = open(path, 'w')
        f.write(description)
        f.close()

    def read_obj(self, path):
        f = open(path, 'r')
        description = f.read().split('\n')
        f.close()
        name = ''
        coordinates = []
        for line in description:
            atr, *value = line.split()
            if atr == 'o':
                name = ' '.join(value)
            else:
                value = list(map(float, value))
                coordinates.append(value[:-1])
        return name, coordinates
