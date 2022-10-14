import './App.css';
import * as React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';

import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';

function App() {
    let defaultConfig = {
        episodes: 10000,

        timesteps: 1500,

        actions: [{
            id: 0,
            name: 'Adelante',
            velocity: 0.3,
            turn: 0,
            reward: 5
        }, {
            id: 1,
            name: 'Izquierda',
            velocity: 0.05,
            turn: 0.3,
            reward: 1
        }, {
            id: 2,
            name: 'Derecha',
            velocity: 0.05,
            turn: -0.3,
            reward: 1
        }],

        algorithms: [{
            name: 'qLearn',
            selected: true
        }, {
            name: 'sarsa',
            selected: false
        }],

        worlds: [{
            name: 'oficina',
            selected: true
        }, {
            name: 'laberinto',
            selected: false
        }, {
            name: 'circuito',
            selected: false
        }]
    }

    const [config, setConfig] = React.useState(defaultConfig);
    const [episodesError, setEpisodesError] = React.useState('');
    const [timestepsError, setTimestepsError] = React.useState('');

    function timestepsOnChange(e) {
        let maxTimesteps = 9999;
        let minTimesteps = 0;
        
        if (e.target.value > minTimesteps && e.target.value <= maxTimesteps) {
            setTimestepsError('');
            setConfig({ ...config, timesteps: parseFloat(e.target.value).toFixed() });
        } else {
            setTimestepsError('Ingresa un valor entero entre 1 y 9999');
        }
    }

    function episodesOnChange(e) {
        let maxEpisodes = 99999;
        let minEpisodes = 0;
        if (e.target.value > minEpisodes && e.target.value <= maxEpisodes) {
            setEpisodesError('');
            setConfig({ ...config, episodes: parseFloat(e.target.value).toFixed() });
        } else {
            setEpisodesError('Ingresa un valor entero entre 1 y 99999');
        }
    }

    function algorithmOnChange(e) {
        let selectedAlgorithm = e.target.value;
        let algorithms = [];
        let i;
        let currentAlgorithm;

        for (i = 0; i < config.algorithms.length; i++) {
            currentAlgorithm = config.algorithms[i].name;

            algorithms.push({
                name: currentAlgorithm,
                selected: currentAlgorithm === selectedAlgorithm
            });
        }

        setConfig({ ...config, algorithms: algorithms });
    }

    function worldsOnChange(e) {
        let selectedWorld = e.target.value;
        let worlds = [];
        let i;
        let currentWorld;

        for (i = 0; i < config.worlds.length; i++) {
            currentWorld = config.worlds[i].name;

            worlds.push({
                name: currentWorld,
                selected: currentWorld === selectedWorld
            });
        }

        setConfig({ ...config, worlds: worlds });
    }

    function generate(cfg, element) {
        return cfg.actions.map((action) =>
            React.cloneElement(element, {
                key: action.id,
                children: [
                    <Grid container spacing={2}>
                        <Grid item xs={3}>
                            <TextField
                                onChange={(event) => updateAction(event)}
                                required
                                inputProps={{
                                    'data-action-id': action.id,
                                    'data-field': 'name'
                                }}
                                value={action.name}
                            />
                        </Grid>
                        <Grid item xs={3}>
                            <TextField
                                onChange={(event) => updateAction(event)}
                                required
                                inputProps={{
                                    'data-action-id': action.id,
                                    'data-field': 'velocity',
                                    'inputMode': 'decimal'  
                                }}
                                value={action.velocity}
                            />
                        </Grid>
                        <Grid item xs={3}>
                            <TextField
                                onChange={(event) => updateAction(event)}
                                required                                                                
                                inputProps={{
                                    'data-action-id': action.id,
                                    'data-field': 'turn',
                                    'inputMode': 'decimal'                                    
                                }}
                                value={action.turn}
                            />
                        </Grid>
                        <Grid item xs={3}>
                            <TextField
                                onChange={(event) => updateAction(event)}
                                required
                                inputProps={{
                                    'data-action-id': action.id,
                                    'data-field': 'reward',
                                    'inputMode': 'numeric'
                                }}
                                value={action.reward}
                            />
                        </Grid>
                    </Grid>
                ]
            })
        );
    }

    const [actionsError, setActionsError] = React.useState({});

    function updateAction(event) {
        let actionId = parseInt(event.target.getAttribute('data-action-id'), 10);
        let actionField = event.target.getAttribute('data-field');
        let value = event.target.value;
        let actions = [...config.actions];
        let found;
        let i = 0;
        let errorFound = false;
        let newActionsError = {...actionsError};
        let velocity;
        let turn;
        let reward;

        while (!found && i < actions.length) {
            let action = actions[i];

            found = action.id === actionId;

            if (!newActionsError[actionId]) {
                newActionsError[actionId] = {};
            }

            if (found) {                
                switch (actionField) {
                    case 'velocity':
                        velocity = parseFloat(value).toFixed(2);

                        if (velocity < 0 || velocity > 1) {
                            newActionsError[actionId].velocity = 'La velocidad debe ser un valor decimal entre 0 y 1';
                        } else {
                            newActionsError[actionId].velocity = null; 
                            action[actionField] = velocity;
                        }
                        
                        break;                        
                    case 'turn': 
                        turn = parseFloat(value).toFixed(2);

                        if (turn < -1 || turn > 1) {
                            newActionsError[actionId].turn = 'El angulo de giro debe ser un valor decimal entre -1 y 1';
                        } else {
                            newActionsError[actionId].turn = null
                            action[actionField] = turn;
                        }
                        break;                                                                 
                    case 'reward':
                        reward = parseFloat(value).toFixed();

                        if (reward < -1000 || reward > 1000) {
                            newActionsError[actionId].reward = 'La recompensa debe ser un valor entero entre -1000 y 1000';
                        } else {
                            newActionsError[actionId].reward = null
                            action[actionField] = reward;
                        }
                        break;                         
                    default: 
                        action[actionField] = value;                      
                }                                     
                
                setActionsError(newActionsError);
                setConfig({ ...config, actions: actions });
            }

            i++;
        }
    }

    function removeAction(actionIdToRemove) {
        let actions=[...config.actions];
        
        actions = actions.filter(action => action.id !== actionIdToRemove);

        setConfig({ ...config, actions: actions });
    }

    function addAction() {
        let actions=[...config.actions];
        let newId = actions.length ? actions[actions.length - 1].id + 1 : 0;

        actions.push({ 
            id: newId,
            name: 'Accion ' + (newId + 1),
            turn: 0,
            velocity: 1,
            reward: 1
        });

        setConfig({ ...config, actions: actions });
    }

    return (
        <div className="App">
            <Box
                component="form"
                sx={{
                    heigth: 720
                }}
                noValidate
                autoComplete="off"
            >
                <Grid container spacing={2}>
                    <Grid xs={4}>
                        <Typography sx={{ mb: 1, textAlign: 'left' }} variant="h7" component="div">
                            Ejecución
                        </Typography>
                        <Grid xs={12}>
                            <TextField
                                required
                                error={!!episodesError}
                                helperText={episodesError}
                                id="outlined-required"
                                label="Episodios"
                                value={config.episodes}
                                onChange={episodesOnChange}
                                type='number'
                                inputProps={{
                                    step: '1'
                                }}        
                            />
                        </Grid>
                        <Grid xs={12}>
                            <TextField
                                required
                                error={!!timestepsError}
                                helperText={timestepsError}
                                id="outlined-required"
                                label="Timesteps"
                                value={config.timesteps}
                                onChange={timestepsOnChange}
                                type='number'
                                inputProps={{
                                    step: '1'
                                }}
                            />
                        </Grid>
                    </Grid>
                    <Grid xs={8}>
                        <Grid item xs={12}>
                            <Typography sx={{ mb: 1, textAlign: 'left' }} variant="h7" component="div">
                                Ambientes
                            </Typography>
                        </Grid>
                        <Grid container>
                            <FormControl>
                                <RadioGroup
                                    row
                                    value={config.worlds.find(x => x.selected).name}
                                    name="radio-buttons-group"
                                >
                                    {
                                        config.worlds.map((world) => {
                                            return <Grid item xs={4} key={world.name}>
                                                <FormControlLabel value={world.name} control={<Radio />} label={world.name} onChange={worldsOnChange} />
                                            </Grid>
                                        })
                                    }
                                </RadioGroup>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12}>
                            <Typography sx={{ mb: 1, textAlign: 'left' }} variant="h7" component="div">
                                Algoritmos
                            </Typography>
                        </Grid>
                        <Grid container>
                            <FormControl>
                                <RadioGroup
                                    row
                                    value={config.algorithms.find(x => x.selected).name}
                                    name="radio-buttons-group"
                                >
                                    {
                                        config.algorithms.map((algorithm) => {
                                            return <Grid item xs={6} key={algorithm.name}>
                                                <FormControlLabel value={algorithm.name} control={<Radio />} label={algorithm.name} onChange={algorithmOnChange} />
                                            </Grid>
                                        })
                                    }
                                </RadioGroup>
                            </FormControl>
                        </Grid>
                    </Grid>
                    <Grid xs={12}>
                        <Grid container>
                            <Typography sx={{ textAlign: 'left' }} variant="h7" component="div">
                                Acciones
                            </Typography>
                            <List dense={false}>
                                {
                                    config.actions.map((action) => (
                                        <ListItem
                                            key={action.id}
                                            secondaryAction={
                                                <IconButton edge="end" aria-label="delete" onClick={() => removeAction(action.id)}> 
                                                    <DeleteIcon />
                                                </IconButton>
                                            }
                                            children={[
                                                <Grid key={'action-fields-' + action.id} container spacing={2}>
                                                    <Grid item xs={3}>
                                                        <TextField
                                                            onChange={(event) => updateAction(event)}
                                                            required
                                                            label='Nombre'
                                                            inputProps={{
                                                                'data-action-id': action.id,
                                                                'data-field': 'name'
                                                            }}
                                                            value={action.name}
                                                        />
                                                    </Grid>
                                                    <Grid item xs={3}>
                                                        <TextField
                                                            onChange={(event) => updateAction(event)}
                                                            required
                                                            error={!!actionsError[action.id]?.velocity}
                                                            helperText={actionsError[action.id]?.velocity}
                                                            label='Velocidad'
                                                            inputProps={{
                                                                'data-action-id': action.id,
                                                                'data-field': 'velocity',
                                                                step: '0.01' 
                                                            }}
                                                            value={action.velocity}
                                                            type='number'
                                                        />
                                                    </Grid>
                                                    <Grid item xs={3}>
                                                        <TextField
                                                            onChange={(event) => updateAction(event)}
                                                            required
                                                            error={!!actionsError[action.id]?.turn}
                                                            helperText={actionsError[action.id]?.turn}
                                                            label='Giro'
                                                            inputProps={{
                                                                'data-action-id': action.id,
                                                                'data-field': 'turn',
                                                                step: '0.01' 
                                                            }}
                                                            value={action.turn}
                                                            type='number'
                                                        />
                                                    </Grid>
                                                    <Grid item xs={3}>
                                                        <TextField
                                                            onChange={(event) => updateAction(event)}
                                                            required
                                                            error={!!actionsError[action.id]?.reward}
                                                            helperText={actionsError[action.id]?.reward}
                                                            label='Recompensa'
                                                            inputProps={{
                                                                'data-action-id': action.id,
                                                                'data-field': 'reward',
                                                                step: '1' 
                                                            }}
                                                            value={action.reward}
                                                            type='number'
                                                        />
                                                    </Grid>
                                                </Grid>
                                            ]}
                                        >
                                        </ListItem>
                                    ))
                                }
                            </List>
                        </Grid>
                    </Grid>
                    <Grid container xs={12}>
                        <Grid xs={3}>
                            <Button
                                onClick={addAction}

                                variant="contained"
                            >
                                Agregar Accion
                            </Button>
                        </Grid>
                        <Grid xs={3}>
                            <Button
                                onClick={() => {
                                    window.loadConfig().then((config) => {
                                        setConfig({ ...defaultConfig, ...config });
                                    });
                                }}

                                variant="contained"
                            >
                                Cargar config
                            </Button>
                        </Grid>

                        <Grid xs={3}>
                            <Button
                                onClick={() => {
                                    setConfig(defaultConfig);
                                }}

                                variant="contained"
                            >
                                Reset config
                            </Button>
                        </Grid>

                        <Grid xs={3}>
                            <Button
                                onClick={() => {
                                    window.triggerProcess(JSON.stringify(config));
                                }}

                                variant="contained"
                            >
                                Comenzar
                            </Button>
                        </Grid>

                        <Grid xs={3}>
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
                </Grid>
            </Box>
        </div>
    );
}

export default App;
