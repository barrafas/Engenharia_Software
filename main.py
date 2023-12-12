from src.app.application import Application
from src.auth.authentication import AuthenticationModule
from src.app.ui import TkinterUI
from src.database.mongo_module import MongoModule
from src.app.state_machine.splash_state import SplashState

if __name__ == '__main__':
    app = Application()
    ui = TkinterUI(app)
    app.ui = ui
    app._state = SplashState(app) # pylint: disable=protected-access
    app.state.render()
    app.run()
   