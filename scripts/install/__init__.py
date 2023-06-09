from .apt.essential import install_apt_essential
from .apt.optional import install_apt_optional

from .source.spdlog import build_and_install_spdlog
from .source.gtest import build_and_install_gtest
from .source.easy_profiler import build_and_install_easy_profiler
from .source.eigen import build_and_install_eigen
from .source.pangolin import build_and_install_pangolin
from .source.opencv import build_and_install_opencv
from .source.ceres import build_and_install_ceres
from .source.gtsam import build_and_install_gtsam
from .source.pcl import build_and_install_pcl

from .python.venv import create_venv
from .python.evo import install_evo