from src.objects.Point3D import Point3D

USER_ORIGIN = Point3D(-40.708927154541016, 53.815513610839844, 548.1220092773438)
USER_DISTANCE = 9.100000381469727

UNKNOWN = 0
FIXATION = 1
SACCADE = 2

SAVE_IMAGE = 0
PLOT_IMAGE = 1

FREQUENCY = 60
BASIC_THRESHOLD = 30

FIXATION_COLUMNS = ['average number of fixations',
                    'minimum value of fixations',
                    'maximum value of fixations',
                    'standard deviation of number of fixations',
                    'dispersion of fixation']
VELOCITY_COLUMNS = ['number of velocities',
                    'average of velocities',
                    'median',
                    'minimum',
                    'maximum',
                    'standard deviation',
                    'dispersion']
