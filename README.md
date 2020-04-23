# test-cloud-functions
Just a repo to prototype the development process for cloud functions.

## Getting Started
Running the scripts in `DevOps` will get your development environment setup. There is one for Windows that assumes [chocolatey](https://chocolatey.org/) is installed. The other is for Linux / WSL.

After this, open the workspace in VSCode and run the install task.

## During Development
All tests will appear in the test explorer on the left. <kbd>F5</kbd> starts the debugger, and will hold at any breakpoints.

Since Cloud Functions are actually triggered by events, one has to be created manually. This is were the `REST Client` extension comes into play. In each function's folder there is a `requests.rest` file with some prefilled requests that the function can be tested against. Simple click `Send Request` at the top of each request to debug the function against that request. The plugin also has the <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>L</kbd> shortcut to repeat the last request.

Finally, there are also some tasks for linting and formating the source files.