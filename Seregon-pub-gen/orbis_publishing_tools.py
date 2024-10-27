import subprocess
import os

class OrbisPublishingTools:
    @staticmethod
    def run_command(command, *args):
        full_command = ["orbis-pub-cmd.exe", command] + list(args)
        result = subprocess.run(full_command, capture_output=True, text=True)
        return result.stdout, result.stderr

    @staticmethod
    def gp4_proj_create(*args):
        return OrbisPublishingTools.run_command("gp4_proj_create", *args)

    @staticmethod
    def gp4_proj_update(*args):
        return OrbisPublishingTools.run_command("gp4_proj_update", *args)

    @staticmethod
    def gp4_playgo_update(*args):
        return OrbisPublishingTools.run_command("gp4_playgo_update", *args)

    @staticmethod
    def gp4_chunk_add(*args):
        return OrbisPublishingTools.run_command("gp4_chunk_add", *args)

    @staticmethod
    def gp4_chunk_update(*args):
        return OrbisPublishingTools.run_command("gp4_chunk_update", *args)

    @staticmethod
    def gp4_chunk_delete(*args):
        return OrbisPublishingTools.run_command("gp4_chunk_delete", *args)

    @staticmethod
    def gp4_scenario_add(*args):
        return OrbisPublishingTools.run_command("gp4_scenario_add", *args)

    @staticmethod
    def gp4_scenario_update(*args):
        return OrbisPublishingTools.run_command("gp4_scenario_update", *args)

    @staticmethod
    def gp4_scenario_delete(*args):
        return OrbisPublishingTools.run_command("gp4_scenario_delete", *args)

    @staticmethod
    def gp4_scenario_setup(*args):
        return OrbisPublishingTools.run_command("gp4_scenario_setup", *args)

    @staticmethod
    def gp4_file_add(*args):
        return OrbisPublishingTools.run_command("gp4_file_add", *args)

    @staticmethod
    def gp4_file_update(*args):
        return OrbisPublishingTools.run_command("gp4_file_update", *args)

    @staticmethod
    def gp4_file_delete(*args):
        return OrbisPublishingTools.run_command("gp4_file_delete", *args)

    @staticmethod
    def gp4_file_sort(*args):
        return OrbisPublishingTools.run_command("gp4_file_sort", *args)

    @staticmethod
    def gp4_batch(*args):
        return OrbisPublishingTools.run_command("gp4_batch", *args)

    @staticmethod
    def gp4_chunk_def_import(*args):
        return OrbisPublishingTools.run_command("gp4_chunk_def_import", *args)

    @staticmethod
    def gp4_chunk_def_export(*args):
        return OrbisPublishingTools.run_command("gp4_chunk_def_export", *args)

    @staticmethod
    def gp4_component_setup(*args):
        return OrbisPublishingTools.run_command("gp4_component_setup", *args)

    @staticmethod
    def gp4_component_add(*args):
        return OrbisPublishingTools.run_command("gp4_component_add", *args)

    @staticmethod
    def gp4_disc_title_add(*args):
        return OrbisPublishingTools.run_command("gp4_disc_title_add", *args)

    @staticmethod
    def gp4_disc_file_add(*args):
        return OrbisPublishingTools.run_command("gp4_disc_file_add", *args)

    @staticmethod
    def sfo_create(*args):
        return OrbisPublishingTools.run_command("sfo_create", *args)

    @staticmethod
    def sfo_export(*args):
        return OrbisPublishingTools.run_command("sfo_export", *args)

    @staticmethod
    def trp_create(*args):
        return OrbisPublishingTools.run_command("trp_create", *args)

    @staticmethod
    def trp_extract(*args):
        return OrbisPublishingTools.run_command("trp_extract", *args)

    @staticmethod
    def trp_compare(*args):
        return OrbisPublishingTools.run_command("trp_compare", *args)

    @staticmethod
    def file_verify(*args):
        return OrbisPublishingTools.run_command("file_verify", *args)

    @staticmethod
    def file_compress(*args):
        return OrbisPublishingTools.run_command("file_compress", *args)

    @staticmethod
    def file_decompress(*args):
        return OrbisPublishingTools.run_command("file_decompress", *args)

    @staticmethod
    def file_check_compress(*args):
        return OrbisPublishingTools.run_command("file_check_compress", *args)

    @staticmethod
    def file_calc_loudness(*args):
        return OrbisPublishingTools.run_command("file_calc_loudness", *args)

    @staticmethod
    def file_digest(*args):
        return OrbisPublishingTools.run_command("file_digest", *args)

    @staticmethod
    def file_estim_refrate(*args):
        return OrbisPublishingTools.run_command("file_estim_refrate", *args)

    @staticmethod
    def file_calc_converted_size(*args):
        return OrbisPublishingTools.run_command("file_calc_converted_size", *args)

    @staticmethod
    def img_create(*args):
        return OrbisPublishingTools.run_command("img_create", *args)

    @staticmethod
    def img_extract(*args):
        return OrbisPublishingTools.run_command("img_extract", *args)

    @staticmethod
    def img_file_list(*args):
        return OrbisPublishingTools.run_command("img_file_list", *args)

    @staticmethod
    def img_verify(*args):
        return OrbisPublishingTools.run_command("img_verify", *args)

    @staticmethod
    def iso_write(*args):
        return OrbisPublishingTools.run_command("iso_write", *args)

    @staticmethod
    def iso_copy(*args):
        return OrbisPublishingTools.run_command("iso_copy", *args)

    @staticmethod
    def pkg_chunk_list(*args):
        return OrbisPublishingTools.run_command("pkg_chunk_list", *args)

    @staticmethod
    def img_info(*args):
        return OrbisPublishingTools.run_command("img_info", *args)

    @staticmethod
    def iso_convert(*args):
        return OrbisPublishingTools.run_command("iso_convert", *args)

    @staticmethod
    def pkg_compare(*args):
        return OrbisPublishingTools.run_command("pkg_compare", *args)

    @staticmethod
    def pkg_compare_delta(*args):
        return OrbisPublishingTools.run_command("pkg_compare_delta", *args)

    @staticmethod
    def pkg_cache_path(*args):
        return OrbisPublishingTools.run_command("pkg_cache_path", *args)

    @staticmethod
    def pkg_cache_create(*args):
        return OrbisPublishingTools.run_command("pkg_cache_create", *args)

    @staticmethod
    def pkg_file_add(*args):
        return OrbisPublishingTools.run_command("pkg_file_add", *args)

    @staticmethod
    def pkg_file_delete(*args):
        return OrbisPublishingTools.run_command("pkg_file_delete", *args)

    @staticmethod
    def pkg_batch(*args):
        return OrbisPublishingTools.run_command("pkg_batch", *args)

    @staticmethod
    def ks_create(*args):
        return OrbisPublishingTools.run_command("ks_create", *args)

    @staticmethod
    def set_conf(*args):
        return OrbisPublishingTools.run_command("set_conf", *args)

    @staticmethod
    def get_conf(*args):
        return OrbisPublishingTools.run_command("get_conf", *args)

    @staticmethod
    def env_info():
        return OrbisPublishingTools.run_command("env_info")

    @staticmethod
    def drive_list(*args):
        return OrbisPublishingTools.run_command("drive_list", *args)

    @staticmethod
    def version(*args):
        return OrbisPublishingTools.run_command("version", *args)

    @staticmethod
    def help(*args):
        return OrbisPublishingTools.run_command("help", *args)

    @staticmethod
    def helpall(*args):
        return OrbisPublishingTools.run_command("helpall", *args)

    @staticmethod
    def projTypeToInfoStr(proj_type, proj_flag):
        # Implementa questa funzione in base alle tue esigenze
        return f"Project Type: {proj_type}, Flag: {proj_flag}"

    @staticmethod
    def progName():
        return "Seregon Publishing Tools"

    @staticmethod
    def progNameSuffix():
        return " - Beta"

    # Aggiungi altri metodi per gli altri comandi necessari

    @staticmethod
    def load_pkg_file(fname):
        return OrbisPublishingTools.pkg_file_list(fname)

    @staticmethod
    def load_sfo_file(fname):
        return OrbisPublishingTools.sfo_export(fname)

    @staticmethod
    def load_pfs_file(fname):
        # Implementa il comando appropriato per i file PFS
        pass

    @staticmethod
    def load_dat_file(fname):
        # Implementa il comando appropriato per i file DAT
        pass
