#!/bin/bash
# To run: cd into parent folder, first time you must type chmod +x run.sh
# afterwards, run using ./run.sh
gnome-terminal --title "Router 1" --window -e "bash -c \"python3 __main__.py Test-2/config1.conf; exec bash\"" &
gnome-terminal --title "Router 2" --window -e "bash -c \"python3 __main__.py Test-2/config2.conf; exec bash\"" &
gnome-terminal --title "Router 3" --window -e "bash -c \"python3 __main__.py Test-2/config3.conf; exec bash\"" &
gnome-terminal --title "Router 4" --window -e "bash -c \"python3 __main__.py Test-2/config4.conf; exec bash\"" &
gnome-terminal --title "Router 5" --window -e "bash -c \"python3 __main__.py Test-2/config5.conf; exec bash\"" &
gnome-terminal --title "Router 6" --window -e "bash -c \"python3 __main__.py Test-2/config6.conf; exec bash\"" &
gnome-terminal --title "Router 7" --window -e "bash -c \"python3 __main__.py Test-2/config7.conf; exec bash\""