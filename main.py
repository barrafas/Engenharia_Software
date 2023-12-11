from src.app.application import Application
from src.auth.authentication import AuthenticationModule
from src.app.ui import TkinterUI
from src.database.mongo_module import MongoModule
from src.database.utils import TimeoutDecorator
from src.app.state_machine.splash_state import SplashState
# from src.app.states.sign_in_up_state import SignInUp

if __name__ == '__main__':
    db = TimeoutDecorator(MongoModule(host="localhost", 
                    port=27017,
                    database_name="test_app"))
    db.connect()
    app = Application(db=db)
    ui = TkinterUI(app)
    app.ui = ui
    app._state = SplashState(app)
    app.state.render()
    app.run()
   