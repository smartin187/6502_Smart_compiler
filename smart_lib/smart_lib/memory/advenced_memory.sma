// Library for read / write advenced value on RAM

import "memory/memory.sma";

.byte_read = 0;
.byte = 0;

void read_advenced: .address_advenced_1, .address_advenced_2, *~string_read_advenced{;

    .byte = 0;

    //while .byte != 21 {;
    //     .byte_read = read_simple: .address_advenced_1, .address_advenced_2 + .byte;
    //     ~string_read_advenced[.byte] = .byte_read;

    //     .byte++;

    //     print: .byte + '0';
    // }

    ~string_read_advenced[0] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[1] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[2] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[3] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[4] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[5] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[6] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[7] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[8] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[9] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[10] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[11] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[12] = read_simple: .address_advenced_1, .address_advenced_2  ;
    .address_advenced_2++;
    ~string_read_advenced[13] = read_simple: .address_advenced_1, .address_advenced_2  ;
    .address_advenced_2++;
    ~string_read_advenced[14] = read_simple: .address_advenced_1, .address_advenced_2;
    .address_advenced_2++;
    ~string_read_advenced[15] = read_simple: .address_advenced_1, .address_advenced_2  ;
    .address_advenced_2++;
    ~string_read_advenced[16] = read_simple: .address_advenced_1, .address_advenced_2  ;
    .address_advenced_2++;
    ~string_read_advenced[17] = read_simple: .address_advenced_1, .address_advenced_2  ;
    .address_advenced_2++;
    ~string_read_advenced[18] = read_simple: .address_advenced_1, .address_advenced_2  ;
    .address_advenced_2++;
    ~string_read_advenced[19] = read_simple: .address_advenced_1, .address_advenced_2 ;
    .address_advenced_2++;
    ~string_read_advenced[20] = read_simple: .address_advenced_1, .address_advenced_2 ;
}

void write_advenced: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced{;

    .byte = 0;

    // while .byte != 21 {;
    //     write_simple: .address_advenced_1_write, .address_advenced_2_write + .byte, ~string_write_advenced[.byte];

    //     .byte++;
    // }

    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[0];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[1];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[2];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[3];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[4];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[5];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[6];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[7];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[8];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[9];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[10];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[11];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[12];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[13];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[14];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[15];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[16];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[17];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[18];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[19];
    .address_advenced_2_write++;
    write_simple: .address_advenced_1_write, .address_advenced_2_write, ~string_write_advenced[20];
}
