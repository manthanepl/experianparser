def writeOffStatus_mapping(write_off_status):
    write_off_status_mapping = { 2: 'Written-off',
                                 6: 'Written Off and Account Sold',
                                 8: 'Account Purchased and Written Off'}
    
    write_off_status = write_off_status_mapping[write_off_status]




    return write_off_status


def suitFiledWillfulDefault_WrittenOff_mapping(SuitFiledWillfulDefaultWrittenOffStatus):
    
    suitFiledWillfulDefaultwo={5 : 'Suit Filed & Written Off',
    6 :'Wilful Default & Written Off',
    7 :'Suit Filed (Wilful Default) & Written Off'}

    SuitFiledWillfulDefaultWrittenOffStatus = suitFiledWillfulDefaultwo[SuitFiledWillfulDefaultWrittenOffStatus]

    return SuitFiledWillfulDefaultWrittenOffStatus


