from app.App import App
from core.Logging import *



logger, handler = setup_logging()
git_manager = GitManager(logger)
app = App(git_manager, logger)
app.mainloop()
teardown_logging(logger, handler)
