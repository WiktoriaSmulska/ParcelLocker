from unittest.mock import MagicMock, patch, mock_open
from src.report_generate import ReportGenerator
from src.service import PurchaseSummaryService
import textwrap
import logging


logging.basicConfig(level=logging.DEBUG)


def test__generate_parcel_sizes_section(purchase_summary_service) -> str:
    """
    Test the _generate_parcel_sizes_section method of ReportGenerator.
    Ensures that the generated section matches the expected format and values.
    """
    report_generator = ReportGenerator(purchase_summary_service)
    result = report_generator._generate_parcel_sizes_section()

    expected_result = textwrap.dedent("""
        === Parcel Sizes ===
        Parcel ID: P12345, Size: LockerComponentsSize.MEDIUM
        Parcel ID: P67890, Size: LockerComponentsSize.MEDIUM
    """)
    assert result.strip() == expected_result.strip()
    return result


def test__generate_locker_usage_section(purchase_summary_service) -> str:
    """
    Test the _generate_locker_usage_section method of ReportGenerator.
    Ensures that the locker usage summary is correctly formatted.
    """
    report_generator = ReportGenerator(purchase_summary_service)
    result = report_generator._generate_locker_usage_section()

    expected_result = textwrap.dedent("""
        === Locker_usage_section ===
        Locker ID: L001, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM
        Locker ID: L002, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM
    """)
    assert result.strip() == expected_result.strip()
    return result


def test__generate_popular_sizes_section(purchase_summary_service) -> str:
    """
    Test the _generate_popular_sizes_section method of ReportGenerator.
    Ensures that the popular sizes section is correctly formatted and contains the expected values.
    """
    report_generator = ReportGenerator(purchase_summary_service)
    result = report_generator._generate_popular_sizes_section()

    expected_result = textwrap.dedent("""
        === Most Frequently Used Parcel Sizes ===
        Locker ID: L001, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM
        Locker ID: L002, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM
    """)
    assert result.strip() == expected_result.strip()
    return result


def test__generate_farthest_users_section(purchase_summary_service) -> str:
    """
    Test the _generate_farthest_users_section method of ReportGenerator.
    Ensures that the section correctly lists the senders and recipients with the farthest deliveries.
    """
    report_generator = ReportGenerator(purchase_summary_service)
    result = report_generator._generate_farthest_users_section()

    expected_result = textwrap.dedent("""
        === Senders and Recipients with Farthest Deliveries ===
        Farthest Senders:
          alice.smith@gmail.com, Farthest Locker: L002, Distance: 2809.5384744134203 km

        Farthest Recipients:
          john.doe@gmail.com, Farthest Locker: L002, Distance: 3944.4215823440827 km
    """)
    assert result.strip() == expected_result.strip()
    return result


def test__generate_longest_delivery_section(purchase_summary_service) -> str:
    """
    Test the _generate_longest_delivery_section method of ReportGenerator.
    Ensures that the longest delivery is accurately represented in the report.
    """
    report_generator = ReportGenerator(purchase_summary_service)
    result = report_generator._generate_longest_delivery_section()

    expected_result = textwrap.dedent("""
        === Longest Delivery ===
        Sender: bob.jones@gmail.com, Longest Delivery Time: 6 days
    """)
    assert result.strip() == expected_result.strip()
    return result


def test_generate_report(purchase_summary_service: PurchaseSummaryService) -> None:
    """
    Test the generate_report method of ReportGenerator.
    Ensures that the complete report is generated and written correctly to a file.
    """
    expected_report = textwrap.dedent("""
            === Parcel Sizes ===
            Parcel ID: P12345, Size: LockerComponentsSize.MEDIUM
            Parcel ID: P67890, Size: LockerComponentsSize.MEDIUM

            === Locker_usage_section ===
            Locker ID: L001, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM
            Locker ID: L002, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM

            === Most Frequently Used Parcel Sizes ===
            Locker ID: L001, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM
            Locker ID: L002, Most Frequently Used Sizes: LockerComponentsSize.MEDIUM

            === Senders and Recipients with Farthest Deliveries ===
            Farthest Senders:
              alice.smith@gmail.com, Farthest Locker: L002, Distance: 2809.5384744134203 km

            Farthest Recipients:
              john.doe@gmail.com, Farthest Locker: L002, Distance: 3944.4215823440827 km

            === Longest Delivery ===
            Sender: bob.jones@gmail.com, Longest Delivery Time: 6 days
        """)

    with patch("builtins.open", mock_open()) as mocked_file:
        report_generator = ReportGenerator(purchase_summary_service)
        report_generator.generate_report("mocked_path.txt")

        mocked_file.assert_called_once_with("mocked_path.txt", "w")

        written_content = mocked_file().write.call_args_list
        actual_report = "".join(call[0][0] for call in written_content)

        assert actual_report.strip() == expected_report.strip()
