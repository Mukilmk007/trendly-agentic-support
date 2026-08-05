from app.controllers.react_controller import ReActController

controller = ReActController()

plan = controller._create_plan(
    "I want to change my delivery address."
)

print(plan)