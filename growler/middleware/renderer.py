
import logging
from pathlib import Path

log = logging.getLogger(__name__)


class Renderer:

    render_engine_map = dict()

    def __init__(self, res):
        """
        Constructor

        Args:
            res (HttpResponse): The response which owns this renderer
        """
        self.res = res
        self.engines = []

    def __call__(self, template, obj=None):
        """
        Should be called via `res.render(...)`.

        This sends the response to the client and will therefore finish the
        growler application chain. An error is raised if no template could be
        found.

        Args:
            template (str): The name of the template to render. If there is no
                file extension, each engine will search for files matching its
                own designated extension.
            obj (dict): A dictionary containing the 'local namespace' of the
                rendering environment.

        Raises:
            ValueError: If no template could be found with the provided name.
        """
        for engine in self.engines:
            filename = engine.find_template_filename(template)
            if filename:
                if obj:
                    self.res.locals.update(obj)
                html = engine.render_source(filename, self.res.locals)
                self.res.send_html(html)
                break
        else:
            raise ValueError("Could not find a template with name '%s'" % template)

    def add_engine(self, engine):
        pass


class RenderEngine:

    def __init__(self, path):
        """
        Constructor

        Args:
            path (str): Top level directory to search for template files - the
                path must exist and the path must be a directory.

        Raises:
            FileNotFoundError: If the provided path does not exists.
            NotADirectoryError: If the path is not a directory.
        """
        self.path = Path(path).resolve()

        if not self.path.is_dir():
            log.warning("path given to render engine is not a directory")
            raise NotADirectoryError("path '%s' is not a directory" % path)

    def __call__(self, req, res):
        """
        The action of this middleware upon client request. The response is
        given a member 'locals' which house the local variables for use in the
        template, and a new method 'render' which takes a template file name
        (relative to the template directory given to the Render's constructor),
        a dict which will update any values in res.locals. After the engine
        runs on this file, the resulting html is sent to the client
        automatically, ending the res/req chain.
        """
        if not hasattr(res, 'render'):
            res.render = Renderer(res)
            res.locals = {}
        res.render.add_engine(self)

    def find_template_filename(self, template_name):
        pass

    def render_source(self, filename, obj):
        """
        Render the template file found at filename.

        Args:
            filename (str): Path to the template file
            obj (dict): Dictionary of data to pass to templating engine

        Returns:
            str: The rendererd file
        """
        raise NotImplementedError()


class StringRenderer(RenderEngine):

    default_file_extensions = [
        '.html.tmpl',
    ]

    def render_source(self, filename, obj=None):
        pass

    def file_text(self, filename):
        pass


Renderer.render_engine_map['string'] = StringRenderer
