import * as React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

class AlgorithmList extends React.Component {
    constructor(props) {
        super(props);
        this.algorithms = props.config.algorithms;
        this.setConfig = props.setConfig;
    }

    render () {
        return (
            <div className='algorithm-radio-container'>
                <FormControl>
                    <FormLabel id="demo-radio-buttons-group-label">Algoritmos</FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="demo-radio-buttons-group-label"
                        defaultValue="qLearn"
                        name="radio-buttons-group"
                    >
                        { 
                            this.algorithms.map((algorithm) => {
                                return <FormControlLabel key={ algorithm.name } value={ algorithm.name } control={<Radio />} label={ algorithm.name } />
                            }) 
                        }
                    </RadioGroup>
                </FormControl>
            </div>
        );
    }
}

export default AlgorithmList;
