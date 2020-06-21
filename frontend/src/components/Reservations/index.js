import React, {useState} from "react"
import {httpCore} from "../../packages/http-core/src"
import useMount from "../../hooks/useMount"
import {
    Dialog,
    DialogTitle,
    DialogActions,
    DialogContent,
    Button,
    DialogContentText,
} from "@material-ui/core"
import moment from 'moment'
import MomentUtils from '@date-io/moment'
import { MuiPickersUtilsProvider, DateTimePicker } from "@material-ui/pickers"
import ReservationsTable from "../ReservationsTable";
import CreateReservationDialog from "../CreateReservationDialog";
import ConfirmReservationDeleteDialog from "../ConfirmReservationDeleteDialog";
import {useSnackbar} from "notistack";


const Reservations = () => {
    const [reservations, setReservations] = useState([])
    const [reservationsPerPage, setReservationsPerPage] = useState(10)
    const [reservationsCount, setReservationsCount] = useState(0)
    const [editingReservationId, setEditingReservationId] = useState(null)
    const [isFetchingData, setIsFetchingData] = useState(true)
    const [reservationsNext, setReservationsNext] = useState(null)
    const [reservationsPrev, setReservationsPrev] = useState(null)
    const [openCreation, setOpenCreation] = useState(false)
    const [reservationToDelete, setReservationToDelete] = useState(null)
    const [showReservationDeleteConfirm, setShowReservationDeleteConfirm] = useState(false)
    const [reservationsPage, setReservationsPage] = useState(0)

    const {enqueueSnackbar} = useSnackbar()

    const getData = async (isPagination= false, page=0, rowsPerPage=reservationsPerPage) => {
        setIsFetchingData(true)
        setOpenCreation(false)
        setReservations([])
        if( !isPagination ) {
            setReservationsPage(0)
        }
        const params = {
            limit: rowsPerPage,
            offset: rowsPerPage*page,
            ordering: 'reserved_from'
        }
        try {
            const reservationsResult = await httpCore.getReservations(params)
            if( reservationsResult.results ) {
                const { count, next, previous, results } = reservationsResult
                setReservations(results)
                setReservationsCount(count)
                setReservationsNext(next)
                setReservationsPrev(previous)
            }
        }
        catch (e) {
            console.log(e)
        } finally {
            setIsFetchingData(false)
        }

    }

    useMount(() => {
        getData()
    })




    const onCancelCreation = () => {
        setOpenCreation(false)
    }


    const onCreate = async (reservedFrom,reservedTo,slot,plateNumber) => {
        const reservation = {
            reserved_from: reservedFrom,
            reserved_to: reservedTo,
            slot,
            plate_number: plateNumber,
        }
        try {
            await httpCore.createReservation(reservation)
            enqueueSnackbar('Reservation Created!', {variant: "success"})
            getData()

        }
        catch (e) {
            enqueueSnackbar('Error in creating reservation!', {variant: "error"})
            console.log(e)
        }
    }


    const onDelete = async () => {
        try {
            await httpCore.deleteReservation(reservationToDelete)
            getData()
        } catch (e) {
            console.log(e)
        } finally {
            setShowReservationDeleteConfirm(false)
            setReservationToDelete(null)
        }
    }



    const onDismissReservationDelete = () => {
        setShowReservationDeleteConfirm(false)
        setReservationToDelete(null)
    }

    const handleReservationsPage = (ev, page) => {
        setReservationsPage(page)
        getData(true, page)
    }

    const handleReservationsRowsPerPage = ev => {
        setReservationsPerPage(ev.target.value)
        getData(false,0, ev.target.value)

    }

    return (
        <MuiPickersUtilsProvider utils={MomentUtils}>
            <>
                <ReservationsTable
                    reservations={reservations}
                    handleReservationsPage={handleReservationsPage}
                    handleReservationsRowsPerPage={handleReservationsRowsPerPage}
                    setEditingReservationId={setEditingReservationId}
                    setShowReservationDeleteConfirm={setShowReservationDeleteConfirm}
                    setReservationToDelete={setReservationToDelete}
                    reservationsCount={reservationsCount}
                    reservationsPerPage={reservationsPerPage}
                    reservationsPage={reservationsPage}
                    reservationsNext={reservationsNext}
                    reservationsPrev={reservationsPrev}
                    setOpenCreation={setOpenCreation}
                    isFetchingData={isFetchingData}
                />

                {openCreation && (
                    <CreateReservationDialog
                        openCreation={openCreation}
                        onCancelCreation={onCancelCreation}
                        onCreate={onCreate}
                    />
                )}
                {showReservationDeleteConfirm && (
                    <ConfirmReservationDeleteDialog
                        showReservationDeleteConfirm={showReservationDeleteConfirm}
                        onDismissReservationDelete={onDismissReservationDelete}
                        onDelete={onDelete}
                    />
                )}

            </>
        </MuiPickersUtilsProvider>
    )
}

export default Reservations