# Hotel-E-Booking

## Hotel_Data.json

    - Room type: Single (S), Double (D), Family (F)
    - Hotel_id = 'H' + stt 
        Ex: H1
    - Room_id = [Hotel_id]_[So phong][Loai]
        Ex: RH1301S 
    - Name file image: [Room_id]_[Number image]

## Bill.json

    - bill_id = 'B'+'Hotel_id'+[number_of_bill]
    Ex: BH1_1

## Format time in this project

    - Time check in and check out: dd/mm/yyyy (in python "%d/%m/%Y")
    - Time for creating bill: "%H:%M:%S %d/%m/%Y"
