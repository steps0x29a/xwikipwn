# xwikipwn
A proof-of-concept XWiki exploit.

This is based on [CVE-2022-36099](https://www.greenbone.net/finder/cve/results/CVE-2022-36099).

# Disclaimer
As usual, this is for educational purposes only. Do not use this on any host you don't own and/or have permission to do so, as using this tool against any other host might be a crime, depending on where you live.
I, the author, am in no way responsible for any of your actions (or lack thereof). TL;DR: don't misuse. I am not responsible. That's about it.

# Usage
Put in the address (`http[s]://...`) of any host with an active XWiki installation and the script will test whether this host is vulnerable. If so, it will give you a very basic shell interface as the user that runs XWiki (most likely the server's tomcat user).

You might have to modify the `xwiki` variable to adjust to your host's URL pattern, depending on the XWiki installation.

# Disclaimer 2
This is a quick and dirty proof of concept and in no way stable or of high quality. Errors are to be expected and the script might destroy your machine, run over your cat or insult your grandmother - in any case, that's your problem :) Use at your own risk. You have been warned :)
