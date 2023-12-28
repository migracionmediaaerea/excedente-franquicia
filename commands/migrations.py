import sys
import os
import manage

sys.argv.append("makemigrations")
sys.argv.extend([f for f in os.listdir("models/") if os.path.isdir("models/"+f)])

manage.main()