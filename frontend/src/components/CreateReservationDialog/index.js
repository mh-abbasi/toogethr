import React, {useState} from "react"
import {
    Button,
    Card, CardContent,
    Dialog, DialogActions,
    DialogContent,
    DialogTitle,
    Grid,
    IconButton,
    TextField,
    Typography
} from "@material-ui/core";
import CloseIcon from "@material-ui/icons/Close";
import {DateTimePicker} from "@material-ui/pickers";
import {makeStyles} from "@material-ui/core/styles";
import moment from "moment";
import {httpCore} from "../../packages/http-core/src";

const useStyles = makeStyles({
    rootDialogFormGrid: {
        flexGrow: 1,
        margin: 0
    },

    textCenter: {
        textAlign: 'center'
    },

    closeButton: {
        position: 'absolute',
        right: '10px',
        top: '10px',
        color: 'gray',
    },

    dialogHead: {
        marginRight: '40px'
    },

    checkAvailability: {
        padding: '7px',
        backgroundColor: '#4caf50',
        "&:hover": {
            backgroundColor: '#54c458'
        }
    },

    detailContainer: {
        display: 'table',
        width: '100%',
    },

    detail: {
        display: 'table-row',
        '& > span': {
            display: 'table-cell',
        }
    },

    slotCard: {
        boxSizing: 'border-box',
        cursor: 'pointer'
    },

    activeSlot: {
        border: '1px solid lightgreen',
    },

    datePicker: {
            width: '100%',
    },
})

const CreateReservationDialog = ({
                                     openCreation,
                                     onCancelCreation,
                                     onCreate,
                                 }) => {
    const [fromDateTime, setFromDateTime] = useState(Date.now())
    const [toDateTime, setToDateTime] = useState(Date.now())
    const [selectedSlot, setSelectedSlot] = useState(null)
    const [plateNumber, setPlateNumber] = useState('')
    const [disableCreation, setDisableCreation] = useState(true)
    const [availableSlots, setAvailableSlots] = useState([])
    const [isCheckingAvailability, setIsCheckingAvailability] = useState(null)

    const classes = useStyles()

    const handleFromChange = date => {
        const newFrom = new Date(date.format("YYYY-MM-DDTHH:mm:ssZ"))
        setFromDateTime(newFrom)
        setDisableCreation(true)
        setSelectedSlot(null)
        setAvailableSlots([])
        setIsCheckingAvailability(null)
    }

    const handleToChange = date => {
        const newTo = new Date(date.format("YYYY-MM-DDTHH:mm:ssZ"))
        setToDateTime(newTo)
        setDisableCreation(true)
        setSelectedSlot(null)
        setAvailableSlots([])
        setIsCheckingAvailability(null)
    }

    const onSlotClick = id => {
        setSelectedSlot(id)
        setDisableCreation(false)
    }

    const onPlateNumberChange = ev => {
        setPlateNumber(ev.target.value)
    }

    const checkAvailability = async () => {
        setAvailableSlots([])
        setIsCheckingAvailability(true)
        try {
            const from = moment(fromDateTime).format('YYYY-MM-DD HH:mm')
            const to = moment(toDateTime).format('YYYY-MM-DD HH:mm')
            const slots = await httpCore.getSlotsAvailability(from, to)
            if( slots ) {
                const {results: availableSlots} = slots
                setAvailableSlots(availableSlots)
            }

        } catch (e) {
            console.log(e)
        } finally {
            setIsCheckingAvailability(false)
        }
    }

    const onSubmit = () => {
        const from = moment(fromDateTime).format('YYYY-MM-DD HH:mm')
        const to = moment(toDateTime).format('YYYY-MM-DD HH:mm')
        onCreate(from, to, selectedSlot, plateNumber)
    }

    return (
        <Dialog open={openCreation} maxWidth={false}>
            <DialogTitle>
                <Typography variant="inherit" className={classes.dialogHead}>Create Reservation</Typography>
                <IconButton aria-label="close" className={classes.closeButton} onClick={onCancelCreation}>
                    <CloseIcon />
                </IconButton>
            </DialogTitle>
            <DialogContent dividers>
                <Grid container justify="center" spacing={2} className={classes.rootDialogFormGrid} >
                    <Grid item xs={12} md={6}>
                        <DateTimePicker
                            label="From"
                            inputVariant="outlined"
                            value={fromDateTime}
                            onChange={handleFromChange}
                            disablePast={true}
                            classes={{root: classes.datePicker}}
                            showTodayButton
                            format='MMM. DD, YYYY HH:mm'
                        />
                    </Grid>
                    <Grid item xs={12} md={6}>
                        <DateTimePicker
                            label="To"
                            inputVariant="outlined"
                            value={toDateTime}
                            onChange={handleToChange}
                            disablePast={true}
                            minDate={fromDateTime}
                            classes={{root: classes.datePicker}}
                            format={'MMM. DD, YYYY HH:mm'}
                        />
                    </Grid>
                    <Grid item xs={12} md={4}>
                        <TextField label="PlateNumber" variant="outlined" value={plateNumber} fullWidth onChange={onPlateNumberChange} />
                    </Grid>
                    <Grid item xs={12} md={12} className={classes.textCenter}>
                        <Button disabled={!!isCheckingAvailability} onClick={checkAvailability} className={classes.checkAvailability}>Check Availability</Button>
                    </Grid>
                    {isCheckingAvailability === false && (
                        availableSlots.length > 0 ? (
                            <Grid item xs={12} md={12} className={classes.slotsContainer}>
                                <Grid container spacing={2}>
                                    {availableSlots.map(slot => {
                                        const isActive = selectedSlot === slot.id ? classes.activeSlot : ''
                                        return (
                                            <Grid item xs={12} md={4} key={slot.id}>
                                                <Card className={`${classes.slotCard} ${isActive}`} onClick={() => onSlotClick(slot.id)}>
                                                    <CardContent>
                                                        <div className={classes.detailContainer}>
                                                            <div className={classes.detail}>
                                                                <span>Slot Floor:</span>
                                                                <span>{slot.floor.toString()}</span>
                                                            </div>
                                                            <div className={classes.detail}>
                                                                <span>Slot Number:</span>
                                                                <span>{slot.number.toString()}</span>
                                                            </div>
                                                            <div className={classes.detail}>
                                                                <span>Slot Coords:</span>
                                                                <span>{slot.coords_title.toString()}</span>
                                                            </div>
                                                        </div>
                                                    </CardContent>
                                                </Card>
                                            </Grid>
                                        )
                                    })}
                                </Grid>
                            </Grid>
                        ) : (<Typography variant="subtitle1" color="error">No available slot for selected time window</Typography> )
                    )}
                </Grid>
            </DialogContent>
            <DialogActions>
                <Button autoFocus disabled={disableCreation} onClick={onSubmit} color="primary">
                    Create
                </Button>
                <Button autoFocus onClick={onCancelCreation} color="secondary">
                    Cancel
                </Button>
            </DialogActions>
        </Dialog>
    )
}

export default CreateReservationDialog