" " " BACKDOOR " " "
2 ways to connect target and kali-bind connection(kali to victim),reverse connection(victim to kali,less suspicious). We'll be building the reverse connection in the WHOLE SESSION.
We are gonna build our own tools. Previously we used veil to create backdoor and then used msfconsole for handling the connection.
Hence we are gonna write our own backdoor(in windows) as well as a listener(in kali) parallelly.
We'll be sending data from windows to kali and from kali to windows as well. We'll be running cmd commands on windows system but from kali.
Using netcat you can run commands like dir,cd,etc. but we cannot run commands like download,upload etc. Hence we'll make our own listener.
For example there's a txt file in windows and we want to view it from kali, it won't display the whole content in case it's too large (too many characters) since it's TCP.
(maybe you can view it by hitting enter again and again after running the program in kali)
So we'll be converting the file into json before sending (json.dumps), and then again json.load after receiving for BOTH kali and windows.
If we misspell the command, we will get an error and we'll lose the connection, hence we'll need to handle this error.