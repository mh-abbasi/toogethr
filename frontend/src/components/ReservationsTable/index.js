import React, {useState} from "react"
import {
    Fab,
    Grid,
    IconButton,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead, TablePagination,
    TableRow,
    Paper
} from "@material-ui/core"
import PlusIcon from "@material-ui/icons/Add"
import moment from "moment"
import EditIcon from "@material-ui/icons/Edit"
import DeleteIcon from "@material-ui/icons/Delete"
import {makeStyles} from "@material-ui/core/styles";
import {getTokenDetails} from "../../hooks/useLoginFlow";

const useStyles = makeStyles({
    isDeleted: {
        backgroundColor: 'rgba(255,0,0,.05)'
    },

    paper: {
        overflow: 'hidden'
    },

    addButton: {
        position: 'fixed',
        bottom: '5px',
        right: '5px',
        zIndex: 10
    },

    tableBlackHeader: {
        backgroundColor: '#000',
        color: '#FFF'
    },
    textCenter: {
        textAlign: "center"
    }

})
const ReservationsTable = ({
                               reservations,
                               handleReservationsPage,
                               handleReservationsRowsPerPage,
                               setEditingReservationId,
                               setShowReservationDeleteConfirm,
                               setReservationToDelete,
                               reservationsCount,
                               reservationsPerPage,
                               reservationsPage,
                               reservationsNext,
                               reservationsPrev,
                               setOpenCreation,
                               isFetchingData
                           }) => {


    const classes = useStyles()
    const {is_superuser} = getTokenDetails()

    const headers = [
        { id: 'id', label: 'ID' },
        { id: 'plate_no', label: 'Plate Number' },
        { id: 'reserved_from', label: 'Reserved From' },
        { id: 'reserved_to', label: 'Reserved To' },
    ]
    if( is_superuser === true ) {
        headers.push({
            id: 'user', label: 'User'
        })
    }

    headers.push({
        id: 'actions', label: 'Actions'
    })

    const onEditClicked = id => {
        setEditingReservationId(id)
    }
    const onConfirmDelete = id => {
        setShowReservationDeleteConfirm(true)
        setReservationToDelete(id)
    }

    const handleAddClick = () => {
        setOpenCreation(true)
    }

    return (
        <Grid container>
            <Grid item xs={12}>
                <Fab color="primary" onClick={handleAddClick} aria-label="add"  className={classes.addButton} >
                    <PlusIcon />
                </Fab>
            </Grid>
            <Grid item xs={12}>
                <Paper className={classes.paper}>
                    <TableContainer>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    {headers.map((headCell) => (
                                        <TableCell
                                            key={headCell.id}
                                            align="left"
                                            padding="default"
                                            className={classes.tableBlackHeader}
                                        >
                                            {headCell.label}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {reservations.length > 0 ?
                                    reservations.map((reservation) => {
                                        const {id, reserved_from, reserved_to, user_data, plate_number, deleted_at} = reservation
                                        const {email} = user_data
                                        const isDeleted = deleted_at ? classes.isDeleted : ''
                                        return (
                                            <TableRow key={id} className={isDeleted}>
                                                <TableCell>{id}</TableCell>
                                                <TableCell>{plate_number}</TableCell>
                                                <TableCell>{moment(reserved_from).format('MMM. DD, YYYY HH:mm')}</TableCell>
                                                <TableCell>{moment(reserved_to).format('MMM. DD, YYYY HH:mm')}</TableCell>
                                                {is_superuser && <TableCell>{email}</TableCell>}
                                                <TableCell>
                                                    <IconButton onClick={()=> onEditClicked(id)}>
                                                        <EditIcon color="primary" />
                                                    </IconButton>
                                                    <IconButton onClick={()=> onConfirmDelete(id)}>
                                                        <DeleteIcon color="error" />
                                                    </IconButton>
                                                </TableCell>
                                            </TableRow>
                                        )
                                    })
                                    :
                                    (<TableRow>
                                        <TableCell className={classes.textCenter} colSpan={headers.length}>
                                            {isFetchingData ? 'Loading reservations...' :'No Reservations Found!'}
                                        </TableCell>
                                    </TableRow>)}
                            </TableBody>
                        </Table>
                    </TableContainer>
                    <TablePagination
                        rowsPerPageOptions={[5, 10, 25]}
                        component="div"
                        count={reservationsCount}
                        rowsPerPage={reservationsPerPage}
                        page={reservationsPage}
                        nextIconButtonProps={{
                            disabled: !!!reservationsNext
                        }}
                        backIconButtonProps={{
                            disabled: !!!reservationsPrev
                        }}
                        onChangePage={handleReservationsPage}
                        onChangeRowsPerPage={handleReservationsRowsPerPage}
                    />
                </Paper>

            </Grid>
        </Grid>
    )
}

export default ReservationsTable