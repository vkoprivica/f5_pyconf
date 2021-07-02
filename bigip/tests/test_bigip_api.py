from bigip.api.device_api import BigipConfig


def test_device() -> None:

    assert BigipConfig(
        'bigip1').authentication().hostname == '192.168.7.72'
    # assert device(
    #     'bigip-node-2').hostname == '192.168.7.73'
