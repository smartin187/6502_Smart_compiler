// Library for read / write advenced value on RAM

import "memory/memory.sma";

.byte_read = 0;

void read_advenced: .address_advenced_1, .address_advenced_2, *~string_read_advenced {;

    for .byte in |0|21|1| {;
        .byte_read = read_simple: .address_advenced_1, .address_advenced_2 + .byte;
        ~string_read_advenced[.byte] = .byte_read;
    }
}
