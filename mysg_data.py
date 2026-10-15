# mysg_data.py - Katalog Rasmi MySG KPM (Sekolah Menengah & Sekolah Rendah)

MYSG_KATALOG = {
    "SEKOLAH_MENENGAH": {
        "PORTFOLIO_BERJAWATAN": [
            # PTA - Pengajaran dan Pentadbiran
            {"kod": "HM01", "nama": "Pengetua (PGB)", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HM02", "nama": "Guru Penolong Kanan Pentadbiran", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HM03", "nama": "Guru Penolong Kanan Hal Ehwal Murid", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HM04", "nama": "Guru Penolong Kanan Kokurikulum", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HM05", "nama": "Guru Penolong Kanan Petang", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HM06", "nama": "Guru Penolong Kanan Pendidikan Khas", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HM10", "nama": "Guru Penolong Kanan Tingkatan 6", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HM12", "nama": "Guru Kanan Mata Pelajaran (GKMP)", "kategori": "PTA", "perkhidmatan": "PPP"},
            
            # PdP - Pengajaran dan Pembelajaran
            {"kod": "HM15", "nama": "Guru Penyelaras Bestari", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HM16", "nama": "Guru Perpustakaan dan Media", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HM17", "nama": "Guru Data", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HM18", "nama": "Guru Tingkatan Enam Akademik", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HM24", "nama": "Guru Akademik KSSM", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HM30", "nama": "Guru Pendidikan Islam", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HM39", "nama": "Guru Pendidikan Khas Integrasi (PPKI)", "kategori": "PdP", "perkhidmatan": "PPP"},
            
            # PTB - Pengurusan & Pentadbiran (GBK & AKP)
            {"kod": "HM52", "nama": "Guru Bimbingan dan Kaunseling", "kategori": "PTB-GBK", "perkhidmatan": "PPP"},
            {"kod": "HM53", "nama": "Pembantu Tadbir (Perkeranian/Operasi)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HM54", "nama": "Pembantu Tadbir (Kewangan)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HM55", "nama": "Juruteknik Komputer", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HM56", "nama": "Pembantu Pengurusan Murid (PPKI)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HM57", "nama": "Pembantu Pengurusan Murid (Asrama)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HM58", "nama": "Pembantu Operasi", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HM59", "nama": "Penyelia Asrama", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HM64", "nama": "Pembantu Makmal", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
        ],
        "PORTFOLIO_TANPA_JAWATAN": [
            # Pengurusan & Pentadbiran
            {"kod": "PM01", "nama": "Guru Kelas", "komponen": "Pentadbiran", "jam_standard": 4.0, "kerumitan": 1.1},
            {"kod": "PM02", "nama": "Guru Bertugas Harian", "komponen": "Pentadbiran", "jam_standard": 2.5, "kerumitan": 1.0},
            {"kod": "PM03", "nama": "Penyelaras PPKI Lantikan Dalaman", "komponen": "Pentadbiran", "jam_standard": 3.0, "kerumitan": 1.2},
            {"kod": "PM04", "nama": "Setiausaha Latihan Dalam Perkhidmatan (SULDP)", "komponen": "Pentadbiran", "jam_standard": 2.0, "kerumitan": 1.1},
            {"kod": "PM05", "nama": "Penyelaras Tingkatan", "komponen": "Pentadbiran", "jam_standard": 2.5, "kerumitan": 1.1},
            {"kod": "PM06", "nama": "Setiausaha Jawatankuasa", "komponen": "Pentadbiran", "jam_standard": 2.0, "kerumitan": 1.0},
            
            # Kurikulum
            {"kod": "PM07", "nama": "Ketua Panitia Mata Pelajaran", "komponen": "Kurikulum", "jam_standard": 3.0, "kerumitan": 1.2},
            {"kod": "PM08", "nama": "Setiausaha Peperiksaan Dalaman", "komponen": "Kurikulum", "jam_standard": 3.5, "kerumitan": 1.3},
            {"kod": "PM09", "nama": "Setiausaha Peperiksaan Awam (SPM/STPM)", "komponen": "Kurikulum", "jam_standard": 4.0, "kerumitan": 1.4},
            {"kod": "PM10", "nama": "Penyelaras ICT Lantikan Dalaman", "komponen": "Kurikulum", "jam_standard": 3.0, "kerumitan": 1.2},
            
            # Hal Ehwal Murid
            {"kod": "PM13", "nama": "Ketua Guru Disiplin", "komponen": "HEM", "jam_standard": 4.0, "kerumitan": 1.3},
            {"kod": "PM14", "nama": "Penyelaras Skim Pinjaman Buku Teks (SPBT)", "komponen": "HEM", "jam_standard": 3.5, "kerumitan": 1.2},
            {"kod": "PM15", "nama": "Warden Asrama", "komponen": "HEM", "jam_standard": 6.0, "kerumitan": 1.4},
            
            # Kokurikulum
            {"kod": "PM16", "nama": "Setiausaha Sukan", "komponen": "Kokurikulum", "jam_standard": 4.0, "kerumitan": 1.3},
            {"kod": "PM17", "nama": "Penyelaras Unit Kokurikulum (Beruniform/Kelab/Sukan)", "komponen": "Kokurikulum", "jam_standard": 3.0, "kerumitan": 1.2},
            {"kod": "PM18", "nama": "Guru Penasihat Unit Kokurikulum", "komponen": "Kokurikulum", "jam_standard": 2.0, "kerumitan": 1.0},
        ],
        "JAWATANKUASA": [
            # Pentadbiran
            {"kod": "JM01", "nama": "JK Pengurusan Sekolah", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM02", "nama": "JK Pengurusan Maklumat Sekolah (JKPMS)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM03", "nama": "JK Pengurusan Sumber Manusia", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM04", "nama": "JK Pengurusan Kewangan, Akaun dan Aset Sekolah (JKPKAS)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.1},
            {"kod": "JM05", "nama": "JK Standard Kualiti Pendidikan Malaysia (SKPM)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM07", "nama": "JK Pengurusan Bencana Sekolah", "komponen": "Pentadbiran", "jam_standard": 1.0, "kerumitan": 1.0},
            {"kod": "JM08", "nama": "JK Persatuan Ibu Bapa dan Guru (PIBG)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.1},
            
            # Kurikulum
            {"kod": "JM21", "nama": "JK Pengurusan Kurikulum", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM22", "nama": "JK Panitia Mata Pelajaran", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM23", "nama": "JK Pentaksiran dan Peperiksaan", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.1},
            {"kod": "JM24", "nama": "JK Pusat Sumber Sekolah (PSS)", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            
            # Hal Ehwal Murid
            {"kod": "JM25", "nama": "JK Pengurusan Hal Ehwal Murid (HEM)", "komponen": "HEM", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM26", "nama": "JK Pengurusan Disiplin Murid", "komponen": "HEM", "jam_standard": 1.5, "kerumitan": 1.1},
            {"kod": "JM27", "nama": "JK Pengurusan 3K (Kebersihan, Kesihatan, Keselamatan)", "komponen": "HEM", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM28", "nama": "JK Bimbingan dan Kaunseling", "komponen": "HEM", "jam_standard": 1.0, "kerumitan": 1.0},
            {"kod": "JM29", "nama": "JK Pengurusan Asrama", "komponen": "HEM", "jam_standard": 2.0, "kerumitan": 1.2},
            
            # Kokurikulum
            {"kod": "JM30", "nama": "JK Pengurusan Kokurikulum", "komponen": "Kokurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM31", "nama": "JK Pembangunan Sukan Sekolah", "komponen": "Kokurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JM32", "nama": "JK Sukan Tahunan Sekolah", "komponen": "Kokurikulum", "jam_standard": 2.0, "kerumitan": 1.2},
            {"kod": "JM33", "nama": "JK Koperasi Sekolah", "komponen": "Kokurikulum", "jam_standard": 2.0, "kerumitan": 1.1},
        ]
    },
    
    "SEKOLAH_RENDAH": {
        "PORTFOLIO_BERJAWATAN": [
            # PTA - Pengajaran dan Pentadbiran
            {"kod": "HR01", "nama": "Guru Besar (PGB)", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HR02", "nama": "Guru Penolong Kanan Pentadbiran", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HR03", "nama": "Guru Penolong Kanan Hal Ehwal Murid", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HR04", "nama": "Guru Penolong Kanan Kokurikulum", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HR05", "nama": "Guru Penolong Kanan Petang", "kategori": "PTA", "perkhidmatan": "PPP"},
            {"kod": "HR06", "nama": "Guru Penolong Kanan Pendidikan Khas", "kategori": "PTA", "perkhidmatan": "PPP"},
            
            # PdP - Pengajaran dan Pembelajaran
            {"kod": "HR08", "nama": "Guru Penyelaras Bestari", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HR09", "nama": "Guru Perpustakaan dan Media", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HR10", "nama": "Guru Data", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HR11", "nama": "Guru Prasekolah", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HR12", "nama": "Guru Akademik KSSR", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HR17", "nama": "Guru Pendidikan Islam", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HR18", "nama": "Guru Pemulihan / Pemulihan Khas", "kategori": "PdP", "perkhidmatan": "PPP"},
            {"kod": "HR19", "nama": "Guru Program Integrasi (PPKI)", "kategori": "PdP", "perkhidmatan": "PPP"},
            
            # PTB - Pengurusan & Pentadbiran (GBK & AKP)
            {"kod": "HR22", "nama": "Guru Bimbingan", "kategori": "PTB-GBK", "perkhidmatan": "PPP"},
            {"kod": "HR24", "nama": "Pembantu Tadbir (Perkeranian/Operasi)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HR25", "nama": "Pembantu Tadbir (Kewangan)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HR26", "nama": "Juruteknik Komputer", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HR27", "nama": "Pembantu Pengurusan Murid (Prasekolah)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HR28", "nama": "Pembantu Pengurusan Murid (PPKI)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HR29", "nama": "Pembantu Pengurusan Murid (Asrama)", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HR30", "nama": "Pembantu Operasi", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
            {"kod": "HR31", "nama": "Penyelia Asrama", "kategori": "PTB-AKP", "perkhidmatan": "AKP"},
        ],
        "PORTFOLIO_TANPA_JAWATAN": [
            # Pengurusan & Pentadbiran
            {"kod": "PR01", "nama": "Guru Kelas", "komponen": "Pentadbiran", "jam_standard": 4.0, "kerumitan": 1.1},
            {"kod": "PR02", "nama": "Guru Bertugas Harian", "komponen": "Pentadbiran", "jam_standard": 2.5, "kerumitan": 1.0},
            {"kod": "PR03", "nama": "Penyelaras PPKI Lantikan Dalaman", "komponen": "Pentadbiran", "jam_standard": 3.0, "kerumitan": 1.2},
            {"kod": "PR04", "nama": "Penyelaras Latihan Dalam Perkhidmatan (SULDP)", "komponen": "Pentadbiran", "jam_standard": 2.0, "kerumitan": 1.1},
            {"kod": "PR05", "nama": "Penyelaras Tahun", "komponen": "Pentadbiran", "jam_standard": 2.5, "kerumitan": 1.1},
            {"kod": "PR06", "nama": "Setiausaha Jawatankuasa", "komponen": "Pentadbiran", "jam_standard": 2.0, "kerumitan": 1.0},
            {"kod": "PR07", "nama": "Guru Bimbingan Lantikan Dalaman", "komponen": "Pentadbiran", "jam_standard": 3.0, "kerumitan": 1.2},
            
            # Kurikulum
            {"kod": "PR08", "nama": "Ketua Panitia Mata Pelajaran", "komponen": "Kurikulum", "jam_standard": 3.0, "kerumitan": 1.2},
            {"kod": "PR09", "nama": "Setiausaha Peperiksaan Dalaman", "komponen": "Kurikulum", "jam_standard": 3.5, "kerumitan": 1.3},
            {"kod": "PR10", "nama": "Setiausaha Peperiksaan Awam", "komponen": "Kurikulum", "jam_standard": 3.5, "kerumitan": 1.3},
            {"kod": "PR11", "nama": "Penyelaras ICT Lantikan Dalaman", "komponen": "Kurikulum", "jam_standard": 3.0, "kerumitan": 1.2},
            {"kod": "PR12", "nama": "Penyelaras Pusat Sumber Sekolah Lantikan Dalaman", "komponen": "Kurikulum", "jam_standard": 3.0, "kerumitan": 1.2},
            
            # Hal Ehwal Murid
            {"kod": "PR14", "nama": "Ketua Guru Disiplin", "komponen": "HEM", "jam_standard": 4.0, "kerumitan": 1.3},
            {"kod": "PR15", "nama": "Penyelaras Skim Pinjaman Buku Teks (SPBT)", "komponen": "HEM", "jam_standard": 3.5, "kerumitan": 1.2},
            {"kod": "PR16", "nama": "Warden Asrama", "komponen": "HEM", "jam_standard": 6.0, "kerumitan": 1.4},
            
            # Kokurikulum
            {"kod": "PR17", "nama": "Setiausaha Sukan", "komponen": "Kokurikulum", "jam_standard": 4.0, "kerumitan": 1.3},
            {"kod": "PR18", "nama": "Penyelaras Unit Kokurikulum (Beruniform/Kelab/Sukan)", "komponen": "Kokurikulum", "jam_standard": 3.0, "kerumitan": 1.2},
            {"kod": "PR19", "nama": "Guru Penasihat Unit Kokurikulum", "komponen": "Kokurikulum", "jam_standard": 2.0, "kerumitan": 1.0},
        ],
        "JAWATANKUASA": [
            # Pentadbiran
            {"kod": "JR01", "nama": "JK Pengurusan Sekolah", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR02", "nama": "JK Pengurusan Maklumat Sekolah (JKPMS)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR03", "nama": "JK Pengurusan Sumber Manusia", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR04", "nama": "JK Pengurusan Kewangan, Akaun dan Aset Sekolah (JKPKAS)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.1},
            {"kod": "JR05", "nama": "JK Standard Kualiti Pendidikan Malaysia (SKPM)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR07", "nama": "JK Pengurusan Prasekolah", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR08", "nama": "JK Pengurusan Bencana Sekolah", "komponen": "Pentadbiran", "jam_standard": 1.0, "kerumitan": 1.0},
            {"kod": "JR09", "nama": "JK Persatuan Ibu Bapa dan Guru (PIBG)", "komponen": "Pentadbiran", "jam_standard": 1.5, "kerumitan": 1.1},
            
            # Kurikulum
            {"kod": "JR12", "nama": "JK Pengurusan Kurikulum", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR13", "nama": "JK Panitia Mata Pelajaran", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR14", "nama": "JK Pentaksiran", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.1},
            {"kod": "JR15", "nama": "JK Pusat Sumber Sekolah (PSS)", "komponen": "Kurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            
            # Hal Ehwal Murid
            {"kod": "JR16", "nama": "JK Pengurusan Hal Ehwal Murid (HEM)", "komponen": "HEM", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR17", "nama": "JK Pengurusan Disiplin Murid", "komponen": "HEM", "jam_standard": 1.5, "kerumitan": 1.1},
            {"kod": "JR18", "nama": "JK Pengurusan 3K (Kebersihan, Kesihatan, Keselamatan)", "komponen": "HEM", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR19", "nama": "JK Bimbingan dan Kaunseling", "komponen": "HEM", "jam_standard": 1.0, "kerumitan": 1.0},
            {"kod": "JR20", "nama": "JK Pengurusan Asrama", "komponen": "HEM", "jam_standard": 2.0, "kerumitan": 1.2},
            
            # Kokurikulum
            {"kod": "JR21", "nama": "JK Pengurusan Kokurikulum", "komponen": "Kokurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR22", "nama": "JK Pembangunan Sukan Sekolah", "komponen": "Kokurikulum", "jam_standard": 1.5, "kerumitan": 1.0},
            {"kod": "JR23", "nama": "JK Sukan Tahunan Sekolah", "komponen": "Kokurikulum", "jam_standard": 2.0, "kerumitan": 1.2},
        ]
    }
}