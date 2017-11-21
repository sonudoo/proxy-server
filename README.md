This is a HTTP proxy server. It is primarily built for 'proxifying' HTTP requests. This project is still under development. The code is well commented for you to understand and modify.

Current Version: 0.1

#Usage

1. Clone the repository to the computer that you want to use as proxy server.
2. Run the script 'proxyserver.py' on the same.
3. In your browser (on your client computer), attach 'http://ip_address_of_your_proxy_server/' in front of the URL that you want to request through Proxy Server.

For example: If you want to visit https://www.imdb.com/ through proxy then type 'http://ip_address_of_your_proxy_server/https://www.imdb.com/' in your browser.

In other words, place the URL that you want to visit after 'http://ip_address_of_your_proxy_server/'

4. You can also setup your host file. For example, I have entered 'ip_address_of_my_proxy_server ps' into my host file. This helps me in accessing the proxy server like this: http://ps/https://www.imdb.com/.

