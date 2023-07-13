from mangadanga.downloader import Mangatown
import pytest

[
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_01.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_02.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_03.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_04.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_05.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_06.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_07.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_08.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_09.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_10.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_11.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_12.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_13.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_14.jpg",
]
# self.get_src_numbers_suffix(first_img_src)

[
    "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_01.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/002-003.0/compressed/fma_03_02.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/003-003.0/compressed/fma_03_03.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/004-003.0/compressed/fma_03_04.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/005-003.0/compressed/fma_03_05.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/006-003.0/compressed/fma_03_06.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/007-003.0/compressed/fma_03_07.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/008-003.0/compressed/fma_03_08.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/009-003.0/compressed/fma_03_09.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/010-003.0/compressed/fma_03_10.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/011-003.0/compressed/fma_03_11.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/012-003.0/compressed/fma_03_12.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/013-003.0/compressed/fma_03_13.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/014-003.0/compressed/fma_03_14.jpg",
]


def test_get_src_numbers_suffix():
    assert False


@pytest.mark.parametrize(
    "base_url, page_index, padding, expected_url",
    [
        pytest.param(
            "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_01.jpg",
            14,
            2,
            "https://zjcdn.mangahere.org/store/manga/32/001-003.0/compressed/fma_03_14.jpg",
        )
    ],
)
def test_extrapolate_image_url(base_url: str, page_index: int, padding: int, expected_url: str):
    downloader = Mangatown(base_url)
    new_url = downloader.extrapolate_image_url(base_url, page_index, padding)
    assert expected_url == new_url


# New exception: letters at the end of the url
[
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_01.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_02.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_03.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_04.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_05.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_06.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_07.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_08.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_09.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_10.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_11.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_12.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_13.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_14.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_15.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_16.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_17.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_18.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_19.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_20.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_21.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_22.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_23.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_24.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_25.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_26.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_27.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_28.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_29.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_30.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_31.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_32.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_33.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_34.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_35.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_36.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_37.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_38.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_39.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_40.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_41.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_42.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_43.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_44.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_45.jpg",
] != [
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_01.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_02.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_03.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_04.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_05.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_06.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_07.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_08.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_09.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_10.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_11.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_12.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_13.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_14.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_15.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_16.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_17.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_18.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_19.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_20.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_21.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_22.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_23.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_24.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_25.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_26.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_27.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_28.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_29.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_30.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_31.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_32.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_33.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_34.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_35.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_36.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_37.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_38.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_39.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_omake01_01.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_omake01_02.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_omake01_03.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma01cover_a.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma01cover_b.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma01cover_c.jpg",
]
{
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_44.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_42.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_43.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_40.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_45.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_04_41.jpg",
}
{
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma01cover_b.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_omake01_01.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma01cover_a.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_omake01_03.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma01cover_c.jpg",
    "https://zjcdn.mangahere.org/store/manga/32/001-004.0/compressed/fma_omake01_02.jpg",
}
