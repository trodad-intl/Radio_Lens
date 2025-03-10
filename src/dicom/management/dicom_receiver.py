import os

from django.core.management.base import BaseCommand
from models import Image_Upload
from pydicom import dcmread
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian
from pynetdicom import AE, evt
from pynetdicom.sop_class import (
    ComputedRadiographyImageStorage,
    CTImageStorage,
    MRImageStorage,
    SecondaryCaptureImageStorage,
    Verification,
)


def handle_store(event):
    """Handle EVT_C_STORE events and save received DICOM files."""
    dataset = event.dataset
    dataset.file_meta = event.file_meta

    patient_id = dataset.get("PatientID", "UnknownID")

    print(f"Received DICOM for PatientID: {patient_id}")
    print("DICOM Metadata:", dataset)

    folder_name = str(patient_id).strip().replace(" ", "_")

    sop_instance_uid = dataset.get("SOPInstanceUID", "UnknownSOP").strip()
    dicom_filename = f"{sop_instance_uid}.dcm"
    dicom_filepath = os.path.join(folder_name, dicom_filename)

    try:
        dicom_file = Image_Upload(Image=dicom_filepath)
        dicom_file.save()
        # dataset.save_as(dicom_filepath, write_like_original=False)
        print(f"Saved DICOM file: {dicom_filepath}")
        return 0x0000
    except Exception as e:
        print(f" Error saving DICOM file: {e}")
        return 0x0112


class Command(BaseCommand):
    help = "Start a DICOM server to receive and store incoming DICOM files"

    def handle(self, *args, **kwargs):
        ae = AE()
        ae.ae_title = b"localhost"

        # All contexts

        ae.add_supported_context(Verification)
        ae.add_supported_context(
            CTImageStorage, [ExplicitVRLittleEndian, ImplicitVRLittleEndian]
        )
        ae.add_supported_context(
            MRImageStorage, [ExplicitVRLittleEndian, ImplicitVRLittleEndian]
        )
        ae.add_supported_context(
            ComputedRadiographyImageStorage,
            [ExplicitVRLittleEndian, ImplicitVRLittleEndian],
        )
        ae.add_supported_context(
            SecondaryCaptureImageStorage,
            [ExplicitVRLittleEndian, ImplicitVRLittleEndian],
        )

        handlers = [(evt.EVT_C_STORE, handle_store)]

        print(" Starting DICOM server on 0.0.0.0:5555 ...")
        ae.start_server(("0.0.0.0", 5555), block=True, evt_handlers=handlers)
