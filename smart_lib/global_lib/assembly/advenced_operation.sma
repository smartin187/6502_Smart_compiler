compiletime define LDA_IMM to A9;
compiletime define LDA_ZP to A5;
compiletime define LDA_ZPX to B5;
compiletime define LDA_ABS to AD;
compiletime define LDA_ABX to BD;
compiletime define LDA_ABY to B9;
compiletime define LDA_INX to A1;
compiletime define LDA_INY to B1;

compiletime define ADC_IMM to 69;
compiletime define ADC_ZP to 65;
compiletime define ADC_ZPX to 75;
compiletime define ADC_ABS to 6D;
compiletime define ADC_ABX to 7D;
compiletime define ADC_ABY to 79;
compiletime define ADC_INX to 61;
compiletime define ADC_INY to 71;

compiletime define AND_IMM to 29;
compiletime define AND_ZP to 25;
compiletime define AND_ZPX to 35;
compiletime define AND_ABS to 2D;
compiletime define AND_ABX to 3D;
compiletime define AND_ABY to 39;
compiletime define AND_INX to 21;
compiletime define AND_INY to 31;

compiletime define ASL_ZP to 06;
compiletime define ASL_ZPX to 16;
compiletime define ASL_ABS to 0E;
compiletime define ASL_ABX to 1E;

compiletime define BIT_ZP to 24;
compiletime define BIT_ABS to 2C;

compiletime define BPL_REL to 10;
compiletime define BMI_REL to 30;
compiletime define BVC_REL to 50;
compiletime define BVS_REL to 70;
compiletime define BCC_REL to 90;
compiletime define BCS_REL to B0;
compiletime define BNE_REL to D0;
compiletime define BEQ_REL to F0;

compiletime define CMP_IMM to C9;
compiletime define CMP_ZP to C5;
compiletime define CMP_ZPX to D5;
compiletime define CMP_ABS to CD;
compiletime define CMP_ABX to DD;
compiletime define CMP_ABY to D9;
compiletime define CMP_INX to C1;
compiletime define CMP_INY to D1;

compiletime define CPX_IMM to E0;
compiletime define CPX_ZP to E4;
compiletime define CPX_ABS to EC;

compiletime define CPY_IMM to C0;
compiletime define CPY_ZP to C4;
compiletime define CPY_ABS to CC;

compiletime define DEC_ZP to C6;
compiletime define DEC_ZPX to D6;
compiletime define DEC_ABS to CE;
compiletime define DEC_ABX to DE;

compiletime define EOR_IMM to 49;
compiletime define EOR_ZP to 45;
compiletime define EOR_ZPX to 55;
compiletime define EOR_ABS to 4D;
compiletime define EOR_ABX to 5D;
compiletime define EOR_ABY to 59;
compiletime define EOR_INX to 41;
compiletime define EOR_INY to 51;

compiletime define INC_ZP to E6;
compiletime define INC_ZPX to F6;
compiletime define INC_ABS to EE;
compiletime define INC_ABX to FE;

compiletime define JMP_ABS to 4C;
compiletime define JMP_IND to 6C;
compiletime define JSR_ABS to 20;

compiletime define LDX_IMM to A2;
compiletime define LDX_ZP to A6;
compiletime define LDX_ZPY to B6;
compiletime define LDX_ABS to AE;
compiletime define LDX_ABY to BE;

compiletime define LDY_IMM to A0;
compiletime define LDY_ZP to A4;
compiletime define LDY_ZPX to B4;
compiletime define LDY_ABS to AC;
compiletime define LDY_ABX to BC;

compiletime define LSR_ZP to 46;
compiletime define LSR_ZPX to 56;
compiletime define LSR_ABS to 4E;
compiletime define LSR_ABX to 5E;

compiletime define ORA_IMM to 09;
compiletime define ORA_ZP to 05;
compiletime define ORA_ZPX to 15;
compiletime define ORA_ABS to 0D;
compiletime define ORA_ABX to 1D;
compiletime define ORA_ABY to 19;
compiletime define ORA_INX to 01;
compiletime define ORA_INY to 11;

compiletime define ROL_ZP to 26;
compiletime define ROL_ZPX to 36;
compiletime define ROL_ABS to 2E;
compiletime define ROL_ABX to 3E;

compiletime define ROR_ZP to 66;
compiletime define ROR_ZPX to 76;
compiletime define ROR_ABS to 6E;
compiletime define ROR_ABX to 7E;

compiletime define SBC_IMM to E9;
compiletime define SBC_ZP to E5;
compiletime define SBC_ZPX to F5;
compiletime define SBC_ABS to ED;
compiletime define SBC_ABX to FD;
compiletime define SBC_ABY to F9;
compiletime define SBC_INX to E1;
compiletime define SBC_INY to F1;

compiletime define STA_ZP to 85;
compiletime define STA_ZPX to 95;
compiletime define STA_ABS to 8D;
compiletime define STA_ABX to 9D;
compiletime define STA_ABY to 99;
compiletime define STA_INX to 81;
compiletime define STA_INY to 91;

compiletime define STX_ZP to 86;
compiletime define STX_ZPY to 96;
compiletime define STX_ABS to 8E;

compiletime define STY_ZP to 84;
compiletime define STY_ZPX to 94;
compiletime define STY_ABS to 8C;
