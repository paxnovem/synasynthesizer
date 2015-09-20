from vispy import app
import vis


app.set_interactive()

cow = vis.Canvas()
cow.show()


# Define selection of possble colors
RED = (0.9, 0.1, 0.1, )
ORANGE = (0.9, 0.5, 0.1, )
YELLOW = (0.9, 0.9, 0.1, )
GREEN = (0.1, 0.9, 0.1, )
TEAL = (0.1, 0.9, 0.5, )
BLUE = (0.1, 0.1, 0.9, )
INDIGO = (0.5, 0.1, 0.9, )
PURPLE = (0.9, 0.1, 0.9, )


while True:
	try:
		input_value = input()
		print(input_value)

		if input_value == "0":
			cow._new_explosion(ORANGE)
		
	except (KeyboardInterrupt, EOFError, SystemExit):
		break
