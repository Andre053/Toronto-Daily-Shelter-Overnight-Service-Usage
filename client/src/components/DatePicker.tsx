import { DatePicker } from "@mui/x-date-pickers"
import { LocalizationProvider } from "@mui/x-date-pickers"
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs"

// selecting start and end dates to filter backend data by
export function DatePickers({startDate, endDate, setStartDate, setEndDate}: {startDate: any, endDate: any, setStartDate: any, setEndDate: any}) {

    const onChangeStartDate = (v: any) => {
        setStartDate(v) 
    }
    const onChangeEndDate = (v: any) => {
        setEndDate(v)
    }
    return (
        <label className='grid content-between'>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DatePicker sx={{width: 200, height: 40}} className='my-10' label='End date' value={endDate} onChange={onChangeEndDate}/>
                <DatePicker sx={{width: 200, height: 40}} className='p-5' label='Start date' value={startDate} onChange={onChangeStartDate}/>
            </LocalizationProvider>
        </label>
    )
}