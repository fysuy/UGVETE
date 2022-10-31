// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
// eslint-disable-next-line import/no-extraneous-dependencies
const { contextBridge, ipcRenderer } = require('electron');

// As an example, here we use the exposeInMainWorld API to expose the browsers
// and node versions to the main window.
// They'll be accessible at "window.versions".
process.once('loaded', () => {
    // White-listed channels.
    const ipc = {
        render: {
            // From render to main.
            send: [
                'triggerProcess',
                'stopProcess'
            ],
            // From main to render.
            receive: [],
            // From render to main and back again.
            sendReceive: [
                'loadConfig',
                'loadProgress'
            ]
        }
    };

    // Exposed protected methods in the render process.
    // Allowed 'ipcRenderer' methods.
    contextBridge.exposeInMainWorld('ipcRender', {
        // From render to main.
        send: (channel, args) => {
            const validChannels = ipc.render.send;
            if (validChannels.includes(channel)) {
                ipcRenderer.send(channel, args);
            }
        },
        // From main to render.
        receive: (channel, listener) => {
            const validChannels = ipc.render.receive;
            if (validChannels.includes(channel)) {
                // Deliberately strip event as it includes `sender`.
                ipcRenderer.on(channel, (event, ...args) => listener(...args));
            }
        },
        // From render to main and back again.
        invoke: (channel, args) => {
            const validChannels = ipc.render.sendReceive;
            let ret;

            if (validChannels.includes(channel)) {
                ret = ipcRenderer.invoke(channel, args);
            }

            return ret;
        }
    });
});
