import argparse
import json
import os
import shutil
import subprocess
import yaml
import rich
from .document_yaml import Document
from .jinja_tools import render, render_from_string, render_markdown_from_string

BUILD_DIR = os.path.join('build', 'endeavor')
HIGHLIGHT_STYLE = os.path.join(os.path.dirname(__file__), 'static', 'custom.theme')


def main():
    # Parse CLI args
    args = cli_parser().parse_args()
    rich.print('[bold yellow]' + '='*79 + '[/bold yellow]')
    print('  Starting document generation ...')
    rich.print('[bold yellow]' + '='*79 + '[/bold yellow]')

    ############################################################################
    # Load the document configuration
    ############################################################################
    if os.path.isdir(args.document):
        document_filepath = os.path.join(args.document, 'document.yaml')
    else:
        document_filepath = args.document

    docgen_yaml = Document(document_filepath)._data
    docgen_root = os.path.dirname(document_filepath)

    print('Document definition loaded.')
    if args.debug:
        print(json.dumps(docgen_yaml, indent=4))

    ############################################################################
    # Copy build assets
    ############################################################################
    rich.print('\n[bold]### [cyan]PRE-COMPILE[/cyan] ###[/bold]\n')
    rich.print('  [bold green]+[/bold green] Copying build assets ...', end=' ')
    copy_build_assets(docgen_root, f'./{BUILD_DIR}')
    print('OK')

    ############################################################################
    # Build the vars object used for templating
    ############################################################################
    rich.print('  [bold green]+[/bold green] Compiling template variables ...', end=' ')
    vars = {
        'document': docgen_yaml.get('document'),
        'config':  docgen_yaml.get('config', {}),
        'env':  docgen_yaml.get('env', {}),
        'data': docgen_yaml.get('data', {}),
        'compiled': {}
    }
    print('OK')

    class Builtins:
        citation_needed = '$^{[\\text{citation needed}]}$'
    vars['builtin'] = Builtins

    ############################################################################
    # Make quick refs
    ############################################################################
    rich.print('  [bold green]+[/bold green] Compiling references ...')
    if 'references' in vars['data'].keys():
        class Ref:
            def __init__(self, citecmd, key):
                self.cmd = citecmd
                self.key = key

            def __repr__(self):
                self.__str__()

            def __str__(self):
                return f'${{\\text{{\\{self.cmd}{{{self.key}}}}}}}$'

            def __add__(self, other):
                """TODO: Should only be or'd with other Ref objects"""
                return Ref(self.cmd, ','.join([self.key, other.key]))

        class Refs:
            def __init__(self):
                super().__init__()
                self._used = {}

            def __getattribute__(self, __name: str):
                if not __name.startswith('_'):
                    #print(f'Using reference {__name} ...')
                    self._used[__name] = True
                    #print(self._used)
                result = super().__getattribute__(__name)
                #print(result)
                return result

            def __getitem__(self, key):
                return self.__getattribute__(key)

        refs = Refs()
        for key, val in vars['data'].get('references', {}).items():
            #def func(self):
            #    self._used[key] = True
            #    return '$\\text{{\\cite{{{key}}}}}$'
            cite_cmd = vars['config'].get('cite_command', 'cite')
            setattr(refs, key, f'${{\\text{{\\{cite_cmd}{{{key}}}}}}}$')
            setattr(refs, key, Ref(cite_cmd, key))
        vars['ref'] = refs
    #print('OK')

    ############################################################################
    # Normalize paths
    ############################################################################
    rich.print('  [bold green]+[/bold green] Normalizing path variable ...')
    for key, val in vars['env'].items():
        if isinstance(val, str) and (val.startswith('./') or val.startswith('../')):
            vars['env'][key] = os.path.abspath(os.path.join(docgen_root, val))
    #print('OK')


    ############################################################################
    ## COMPILE
    ############################################################################
    rich.print('\n[bold]### [cyan]COMPILE[/cyan] ###[/bold]\n')

    ############################################################################
    # Compile the appendices Markdown to Tex
    ############################################################################
    rich.print('  [bold green]+[/bold green] Compiling appendices ...')
    rich.print('  [bold green]+[/bold green] Compiling Markdown blob ...')
    with open(f"./{BUILD_DIR}/ev-partials_appendices.md", 'w') as f:
        appendices = docgen_yaml.get("document", {}).get('appendices', [])
        if appendices is None:
            appendices = []
        for i in appendices:
            fpath = os.path.abspath(os.path.join(docgen_root, i))
            rich.print(f'    ... {fpath}')
            md = open(fpath).read()
            md_compiled = render_from_string(md, **vars)
            f.write(md_compiled)
            f.write("\n\n")
    #print('OK')
    if appendices is None or len(appendices) == 0:
        rich.print('    ... [bold red]No appendices found.[/bold red]')
    else:
        rich.print('  [bold green]+[/bold green] Compiling appendices to tex ...')
        make_doc('ev-partials_appendices.md', 'ev-partials_appendices', use_template=False, format='tex', vars=vars)
        vars['compiled']['appendices'] = open(f'./{BUILD_DIR}/ev-partials_appendices.tex').read()
        #print('OK')

    ############################################################################
    # Compile the markdown files into the single body markdown
    ############################################################################
    rich.print('  [bold green]+[/bold green] Compiling body Markdown blob ...')
    with open(f"./{BUILD_DIR}/index.md", 'w') as f:
        for i in docgen_yaml["document"]["body"]:
            fpath = os.path.abspath(os.path.join(docgen_root, i))
            rich.print(f'    ... {fpath}')
            md = open(fpath).read()
            md_compiled = render_markdown_from_string(md, docgen_root, **vars)
            f.write(md_compiled)
            f.write("\n\n")
    #print('OK')

    ############################################################################
    # Compile the tex template
    ############################################################################
    print('')
    rich.print('  [bold green]+[/bold green] Used references:', end=' ')
    if 'ref' in vars.keys():
        rich.print('[dim]' + ', '.join(list(vars['ref']._used.keys())) + '[/dim]')
    print('')

    rich.print('  [bold green]+[/bold green] Compiling tex template ...', end=' ')
    compile_template(docgen_yaml, vars)
    print('OK')

    ############################################################################
    # Build the final document with Pandoc
    ############################################################################
    rich.print('  [bold green]+[/bold green] Compiling final output document with PanDoc ...')
    doc_name =  make_document_title(docgen_yaml)
    result = make_doc('index.md', doc_name, format=args.output_type, vars=vars, debug=args.debug)
    rich.print('[green]Complete[/green].')


def compile_template(docgen_yaml, vars):
    template_name = docgen_yaml['endeavor']['template']
    src = os.path.join(os.path.dirname(__file__), 'templates', template_name)
    dst = f'./{BUILD_DIR}'
    copy_files(src, dst)

    template = open(f'./{BUILD_DIR}/main.jinja.tex').read()
    #print(template)
    #print(vars)
    result = render_from_string(template, **vars)
    #print(result)r
    with open(f"./{BUILD_DIR}/docgen.tex", "w") as f:
        f.write(result)


def compile_markdown(docgen_yaml, docgen_root):
    pass


def make_document_title(docgen_yaml):
    doc_id = docgen_yaml['document'].get('doc_id', None)
    title = docgen_yaml['document']['title']
    title = title.lower()
    title = title.replace(':', '').replace(' ', '-')
    result = f'{doc_id}_{title}' if doc_id is not None else title
    return result



def make_doc(input_file, document_name, format='pdf', use_template=True, vars=None, debug=False):
    if format not in ['pdf', 'tex', 'md']:
        raise Exception(f'Invalid output format: {format}')
    hide_output = False if debug else True
    mermaid_filter = '-F mermaid-filter' if has_mermaid_filter() else ''
    geometry = '-V geometry:"top=2cm, bottom=5cm, left=2cm, right=2cm"'
    template =  '--template=docgen.tex' if use_template else ''
    chapters = '--top-level-division=chapter' if vars.get('config').get('chapters') else ''
    shift_headings = f"--shift-heading-level-by={vars.get('config').get('shift_heading')}" if vars.get('config').get('shift_heading') else ''
    #  --highlight-style {HIGHLIGHT_STYLE} \
    pandoc_args = f"""./{input_file} \
        --pdf-engine pdflatex \
        {template} \
        {chapters} \
        -V colorlinks=true \
        -V linkcolor=MidnightBlue \
        -V urlcolor=MidnightBlue \
        -V toccolor=blue \
        -V linestretch=1.0 \
        -V links-as-notes=true \
        --highlight-style {HIGHLIGHT_STYLE} \
        {geometry} {mermaid_filter} {shift_headings} \
        -o ./{document_name}.{format}
    """
    cmd = f"pandoc {pandoc_args}"
    #print('Running pandoc command ...')
    #print(cmd)
    rich.print(f'  [bold green]+[/bold green] Running PanDoc: [dim white]{cmd}[/dim white]')
    subprocess.run(cmd, shell=True, check=True, cwd=f"./{BUILD_DIR}", capture_output=hide_output)  # cwd=None


def has_mermaid_filter():
    p = subprocess.run('which mermaid-filter', shell=True, capture_output=True)
    return p.returncode == 0


def cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="enable debug mode")
    parser.add_argument('document', help="the docgen.yaml")
    parser.add_argument('--output-type', default="pdf", help="the docgen.yaml")
    return parser


def copy_files(src, dst):
    os.makedirs(dst, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def copy_build_assets(doc_root, build_root):
    os.makedirs(build_root, exist_ok=True)
    try:
        src = os.path.join(doc_root, 'assets')
        dst = os.path.join(build_root, 'assets')
        shutil.copytree(src, dst, dirs_exist_ok=True)
    except FileNotFoundError as e:
        pass


if __name__ == '__main__':
    main()
