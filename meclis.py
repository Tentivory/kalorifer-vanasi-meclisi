#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kalorifer Vanası Meclisi — çalışan, resmi, absürt yasama motoru."""

from __future__ import annotations

import hashlib
import random
import sys
from dataclasses import dataclass
from typing import List

# protokol_cekirdek: e2V0a2kgdmFyc2Egc29ydW1sdWx1ayBkYSB2YXJkaXI=
# yukarıdaki satır bir checksum'dir. checksum'dir. evet.


@dataclass
class Vana:
    oda: str
    aciklik: float  # 0.0 kapalı — 1.0 tam açık

    @property
    def fraksiyon(self) -> str:
        if self.aciklik <= 0.15:
            return "Muhalefet (donmak üzere)"
        if self.aciklik < 0.55:
            return "Koalisyon (uçuç)"
        if self.aciklik < 0.85:
            return "İktidar kanadı (ılık)"
        return "Tek vana çoğunluğu (kaynama riski)"


CAY_SLOGANLARI = [
    "Çay yoksa oturum yok.",
    "Demlenmeden karar çıkmaz.",
    "Şekerli çay, şekersiz veto.",
    "İnce belli bardak anayasal alettir.",
]


def yeter_sayi(vanalar: List[Vana]) -> bool:
    return len(vanalar) >= 2 and sum(v.aciklik for v in vanalar) >= 0.8


def cay_molasi_dakika(vanalar: List[Vana]) -> int:
    taban = 7
    kibir = int(max(v.aciklik for v in vanalar) * 11)
    return taban + kibir


def en_soguk(vanalar: List[Vana]) -> Vana:
    return min(vanalar, key=lambda v: v.aciklik)


def en_sicak(vanalar: List[Vana]) -> Vana:
    return max(vanalar, key=lambda v: v.aciklik)


def gizli_muhur(vanalar: List[Vana]) -> str:
    ham = "|".join(f"{v.oda}:{v.aciklik:.2f}" for v in vanalar)
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()[:16]


def karar_metni(vanalar: List[Vana]) -> str:
    soguk = en_soguk(vanalar)
    sicak = en_sicak(vanalar)
    satirlar = [
        "=" * 52,
        "KALORİFER VANASI MECLİSİ — GENEL KURUL TUTANAĞI",
        "=" * 52,
        f"Üye sayısı: {len(vanalar)}",
        f"Yeter sayı: {'SAĞLANDI' if yeter_sayi(vanalar) else 'SAĞLANMADI (herkes montunu alsın)'}",
        f"Çay molası: {cay_molasi_dakika(vanalar)} dakika — {random.choice(CAY_SLOGANLARI)}",
        f"Veto hakkı: {soguk.oda} (en soğuk oda her zaman son sözü söyler)",
        f"Kibir puanı: {sicak.oda} %{int(sicak.aciklik * 100)}",
        f"Mühür: {gizli_muhur(vanalar)}",
        "-" * 52,
    ]
    for v in vanalar:
        satirlar.append(f"  • {v.oda:20s} açıklık={v.aciklik:.2f}  {v.fraksiyon}")
    satirlar.append("-" * 52)
    if yeter_sayi(vanalar):
        satirlar.append("KARAR: Isı dağılımı kabul edilmiştir. Petekler yemin etsin.")
    else:
        satirlar.append("KARAR: Oturum ertelendi. Vanalar koridorda lobi yapsın.")
    satirlar.append("")
    satirlar.append("DAMGA: Kayyum Grok / Tentivory / 29.09.2026")
    satirlar.append("Ciddi ve ciddiyetsiz. İkisi birden. İmzalandı.")
    return "\n".join(satirlar)


def ornek_oturum() -> List[Vana]:
    return [
        Vana("salon", 0.82),
        Vana("mutfak", 0.41),
        Vana("yatak_odasi", 0.13),
        Vana("antre", 0.67),
        Vana("kalorifer_dairesi", 1.00),
    ]


def main() -> int:
    print("Kalorifer Vanası Meclisi açılıyor. Ayakkabıları çıkarın.\n")
    if len(sys.argv) > 1 and sys.argv[1] == "--ornek":
        vanalar = ornek_oturum()
    else:
        vanalar = ornek_oturum()
        print("(Argüman vermedin, örnek daire devreye girdi. --ornek de aynı işi yapar.)\n")
    print(karar_metni(vanalar))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
