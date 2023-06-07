import json
import os
import yaml


class Document:
    def __init__(self, fpath):

        with open(fpath) as f:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            data = yaml.load(f, Loader=DocGenLoader)

        # Validate yaml
        self.validate_yaml(data)
        print('Document definition validated.')

        self._data = data


    def validate_yaml(self, data):
        ev = data.get('endeavor', None)
        if ev is None:
            raise Exception('Missing section in endeavor docgen: "endeavor" not found.')
        ev_version = ev.get('version', None)
        if ev_version is None:
            raise Exception('Missing section in endeavor docgen: "endeavor.version" not found.')


class DocGenLoader(yaml.FullLoader):

    def __init__(self, stream):

        self._root = os.path.split(stream.name)[0]

        super(DocGenLoader, self).__init__(stream)

    def var_handler(self, node):
        #filename = os.path.join(self._root, self.construct_scalar(node))
        #with open(filename, 'r') as f:
        #    return yaml.load(f, Loader)
        #print(node)
        #return 'foo'
        print('----')
        value = self.construct_scalar(node)
        print(json.dumps(dir(self), indent=4))
        print(self.scan_tag_directive_value('vars'))
        print(value)
        print('-/-/-')
        return 'foo s'

    def include_handler(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, DocGenLoader)
        #print(node)
        #return None
        #print('----')
        #value = self.construct_scalar(node)
        #print(json.dumps(dir(self), indent=4))
        #print(self.scan_tag_directive_value('vars'))
        #print(value)
        #print('-/-/-')
        #return 'foo s'


DocGenLoader.add_constructor('!Include', DocGenLoader.include_handler)
