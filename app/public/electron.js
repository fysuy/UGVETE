// Module to control the application lifecycle and the native browser window.
const { app, BrowserWindow, protocol, ipcMain, ipcRenderer, dialog } = require("electron");
const path = require("path");
const url = require("url");
const { spawn } = require('child_process');
const fs = require('fs');

let processes = [];
let mainWindow;

// Create the native browser window.
function createWindow() {
    mainWindow = new BrowserWindow({
        width: 992,
        height: 720,
        // Set the path of an additional "preload" script that can be used to
        // communicate between node-land and browser-land.
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true
        },
    });

    // In production, set the initial browser path to the local bundle generated
    // by the Create React App build process.
    // In development, set it to localhost to allow live/hot-reloading.
    const appURL = app.isPackaged
        ? url.format({
            pathname: path.join(__dirname, "index.html"),
            protocol: "file:",
            slashes: true,
        })
        : "http://localhost:3000";
    mainWindow.loadURL(appURL);

    // Automatically open Chrome's DevTools in development mode.
    if (!app.isPackaged) {
        mainWindow.webContents.openDevTools();
    }
}

// Setup a local proxy to adjust the paths of requested files when loading
// them from the local production bundle (e.g.: local fonts, etc...).
function setupLocalFilesNormalizerProxy() {
    protocol.registerHttpProtocol(
        "file",
        (request, callback) => {
            const url = request.url.substr(8);
            callback({ path: path.normalize(`${__dirname}/${url}`) });
        },
        (error) => {
            if (error) console.error("Failed to register protocol");
        }
    );
}

// This method will be called when Electron has finished its initialization and
// is ready to create the browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    createWindow();
    setupLocalFilesNormalizerProxy();

    app.on("activate", function () {
        // On macOS it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// Quit when all windows are closed, except on macOS.
// There, it's common for applications and their menu bar to stay active until
// the user quits  explicitly with Cmd + Q.
app.on("window-all-closed", function () {
    if (process.platform !== "darwin") {
        app.quit();
    }
});

// If your app has no need to navigate or only needs to navigate to known pages,
// it is a good idea to limit navigation outright to that known scope,
// disallowing any other kinds of navigation.
const allowedNavigationDestinations = "https://my-electron-app.com";
app.on("web-contents-created", (event, contents) => {
    contents.on("will-navigate", (event, navigationUrl) => {
        const parsedUrl = new URL(navigationUrl);

        if (!allowedNavigationDestinations.includes(parsedUrl.origin)) {
            event.preventDefault();
        }
    });
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
ipcMain.on("triggerProcess", (e, data) => {
    let algorithm;
    let gzclient;

    fs.writeFileSync('config.json', data);

    data = JSON.parse(data);

    for (let index = 0; index < data.worlds.length; index++) {
        let world = data.worlds[index];
        
        if (world.selected) {
            switch (world.name) {
                case 'oficina':
                    process.env['GYM_GAZEBO_WORLD_UGVETE'] = process.env.UGVETE_HOME + "/gym_gazebo/envs/assets/worlds/office.world";
                    break;
                case 'laberinto':
                    process.env['GYM_GAZEBO_WORLD_UGVETE'] = process.env.UGVETE_HOME + "/gym_gazebo/envs/assets/worlds/maze.world";
                    break;
                case 'circuito':
                    process.env['GYM_GAZEBO_WORLD_UGVETE'] = process.env.UGVETE_HOME + "/gym_gazebo/envs/assets/worlds/round.world";
                    break;
                default:
                    break;
            }
        }
    }

    algorithm = spawn("python", [process.env.UGVETE_HOME + "/turtlebot/circuit2_turtlebot_lidar_qlearn.py"]);

    gzclient = spawn("gzclient", ["--verbose"]);
    
    processes.push(algorithm);
    processes.push(gzclient);
    
    algorithm.stdout.on('data', function(data) {
        console.log(data.toString())
    })

    gzclient.stdout.on('data', function(data) {
        console.log(data.toString())
    })
});

ipcMain.on("stopProcess", (e) => {
    for (let index = 0; index < processes.length; index++) {
        processes[index].kill(9);
    }

    spawn("killall", ["-9", "rosout", "roslaunch", "rosmaster", "gzserver", "nodelet", "robot_state_publisher", "gzclient"]);
});

ipcMain.handle("loadConfig", (e) => {
    let file = dialog.showOpenDialogSync(mainWindow, {
        properties: ['openFile'],
        defaultPath: process.env.UGVETE_HOME
    });

    return JSON.parse(fs.readFileSync(file[0]));
});