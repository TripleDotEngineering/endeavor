import jinja2
import os

env = jinja2.Environment(
    loader=jinja2.PackageLoader("endeavor"),
    autoescape=False, #autoescape=jinja2.select_autoescape(),
    variable_start_string='${{',
    block_start_string='<?ev',
    block_end_string='?>',
    comment_start_string='<//',
    comment_end_string='//>'
)


def render(template, **kwargs):
    t = env.get_template(template)
    return t.render(**kwargs)

def render_from_string(s, **kwargs):
    t = env.from_string(s)
    return t.render(**kwargs)

def render_markdown_from_string(s, root, **kwargs):
    #print(os.path.abspath(os.curdir))
    local_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([
            os.path.join(root, "templates")
        ]),
        autoescape=False, #autoescape=jinja2.select_autoescape(),
        variable_start_string='${{',
        block_start_string='<?ev',
        block_end_string='?>',
        comment_start_string='<//',
        comment_end_string='//>'
    )
    t = local_env.from_string(s)
    return t.render(**kwargs)


