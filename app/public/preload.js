// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
// eslint-disable-next-line import/no-extraneous-dependencies
const { contextBridge, ipcRenderer } = require('electron');

// As an example, here we use the exposeInMainWorld API to expose the browsers
// and node versions to the main window.
// They'll be accessible at "window.versions".
process.once('loaded', () => {
    contextBridge.exposeInMainWorld('triggerProcess', (config) => {
        ipcRenderer.send('triggerProcess', config);
    });

    contextBridge.exposeInMainWorld('stopProcess', () => {
        ipcRenderer.send('stopProcess');
    });

    contextBridge.exposeInMainWorld('loadConfig', () => ipcRenderer.invoke('loadConfig'));
});
