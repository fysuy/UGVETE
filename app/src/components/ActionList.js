import * as React from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import IconButton from '@mui/material/IconButton';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import DeleteIcon from '@mui/icons-material/Delete';
import TextField from '@mui/material/TextField';

class ActionList extends React.Component {
    constructor(props) {
        super(props);
        this.setConfig = props.setConfig;
        this.actions = props.config.actions;
    }

    updateAction(event) {
        let actionId = parseInt(event.target.getAttribute('data-action-id'), 10);
        let value = event.target.value;
        let found;
        let i = 0;
    
        while (!found && i < this.actions.length) {
            found = this.actions[i].id === actionId;
    
            if (found) {
                this.actions[i].name = value;
                this.setConfig({ actions: this.actions });
            }
    
            i++;
        }
    }

    generate(element) {
        return this.actions.map((action) =>
            React.cloneElement(element, {
                key: action.name,
                children: [
                    <Grid container>
                        <Grid item xs={4} pr={5}>
                            <TextField
                                onChange={ (event) => this.updateAction(event) }
                                required
                                inputProps={{
                                    'data-action-id': action.id
                                }}
                                defaultValue={action.name}
                            />
                        </Grid>
                        <Grid item xs={4} pr={5}>
                            <TextField
                                onChange={ (event) => this.updateAction(event) }
                                required
                                inputProps={{
                                    'data-action-id': action.id
                                }}
                                defaultValue={action.velocity}
                            />
                        </Grid>
                        <Grid item xs={4} pr={5}>
                            <TextField
                                onChange={ (event) => this.updateAction(event) }
                                required
                                inputProps={{
                                    'data-action-id': action.id
                                }}
                                defaultValue={action.turn}
                            />
                        </Grid>
                        <Grid item xs={4} pr={5}>
                            <TextField
                                onChange={ (event) => this.updateAction(event) }
                                required
                                inputProps={{
                                    'data-action-id': action.id
                                }}
                                defaultValue={action.reward}
                            />
                        </Grid>
                    </Grid>
                ]
            })
        );
    }

    render() {
        return (
            <div>
                <Grid item xs={12} md={6}>
                    <Typography sx={{ textAlign: 'left' }} variant="h7" component="div">
                        Acciones
                    </Typography>
                    <List dense={ false }>
                        {this.generate(
                            <ListItem
                                secondaryAction={
                                    <IconButton edge="end" aria-label="delete">
                                        <DeleteIcon />
                                    </IconButton>
                                }
                            >
                            </ListItem>
                        )}
                    </List>
                </Grid>
            </div>
        );
    }
}

export default ActionList;