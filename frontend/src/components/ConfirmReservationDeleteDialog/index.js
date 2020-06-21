import React from "react"
import {Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle} from "@material-ui/core";

const ConfirmReservationDeleteDialog = ({
                                            showReservationDeleteConfirm,
                                            onDismissReservationDelete,
                                            onDelete
                                        }) => {
    return (
        <Dialog
            open={showReservationDeleteConfirm}
            onClose={onDismissReservationDelete}
            aria-labelledby="delete-reservation-title"
            aria-describedby="delete-reservation-description"
        >
            <DialogTitle id="delete-reservation-title">Are you sure you want to delete it?</DialogTitle>
            <DialogContent>
                <DialogContentText id="delete-reservation-description" color="error">
                    If you delete it, There is no way to get it back!
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={onDismissReservationDelete} color="primary">
                    Nopppee!
                </Button>
                <Button onClick={onDelete} color="secondary" autoFocus>
                    Delete
                </Button>
            </DialogActions>
        </Dialog>
    )
}

export default ConfirmReservationDeleteDialog