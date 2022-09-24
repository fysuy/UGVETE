import './App.css';
import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import AlgorithmList from './components/AlgorithmList';
import ActionList from './components/ActionList';
import Grid from '@mui/material/Unstable_Grid2';

function App() {
    const [config, setConfig] = React.useState({
        episodes: 10000,

        timesteps: 1500,
        
        actions: [{
            id: 0,
            name: 'Adelante',
            velocity: 0.3,
            turn: 0,
            reward: 5,
            enabled: true
        }, {
            id: 1,
            name: 'Izquierda',
            velocity: 0.05,
            turn: 0.3,
            reward: 1,
            enabled: true
        }, {
            id: 2,
            name: 'Derecha',
            velocity: 0.05,
            turn: -0.3,
            reward: 1,
            enabled: true
        }],

        algorithms: [{
            name: 'qLearn',
            selected: true
        }, {
            name: 'sarsa',
            selected: false
        }]
    });

    function timestepsOnChange(e) {
        setConfig({ timesteps: e.target.value });
    }

    function episodesOnChange(e) {
        setConfig({ episodes: e.target.value });
    }

    return (
        <div className="App">
            <Box
                component="form"
                sx={{
                    height: 480,
                }}
                noValidate
                autoComplete="off"
            >
                <Grid container spacing={2}>
                    <Grid xs={3}>
                        <TextField
                            required
                            id="outlined-required"
                            label="Episodios"
                            defaultValue={ config.episodes }
                            onChange={ episodesOnChange }
                        />
                    </Grid>
                    <Grid xs={3}>
                        <TextField
                            required
                            id="outlined-required"
                            label="Timesteps"
                            defaultValue={ config.timesteps }
                            helperText="Por episodio"
                            onChange={ timestepsOnChange }
                        />
                    </Grid>
                    <Grid xs={6}>
                        <AlgorithmList setConfig={ setConfig } config={ config } />
                    </Grid>
                    <Grid xs={12}>
                        <ActionList setConfig={ setConfig } config={ config } />
                    </Grid>
                    <Grid xs={12}>
                        <Button
                            onClick={() => {
                                window.triggerProcess(JSON.stringify(config));
                            }}

                            variant="contained"
                        >
                            Comenzar
                        </Button>
                        <Button
                            onClick={() => {
                                window.stopProcess();
                            }}

                            variant="contained"
                        >
                            Detener
                        </Button>
                    </Grid>
                </Grid>
            </Box>
        </div>
    );
}

export default App;
