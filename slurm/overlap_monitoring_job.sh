#!/bin/bash
#SBATCH --job-name=nicam_dc_perf_01
#SBATCH --output=nicam_dc_perf_01.out
#SBATCH --error=nicam_dc_perf_01.err
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=01:00:00
#SBATCH --mem=120G

# From an assignment to the HPC master online. It worked fine on CESGA
# FinisTerrae III. Based on another snippet by Manuel Gimenez.

# Exit on errors, unset variables
set -eu

# Simple logging function
log() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2
}

log "Loading modules..."
module purge
module load cesga/2022 gcccore/system intel/2023.2.1 impi/2021.10.0

export OMP_NUM_THREADS=1

# Environment variables
NICAM_ROOT=/mnt/netapp2/Store_uni/home/ulc/cursos/curso348/nicamdc
GL=05
RL=02
PROCS=32
GRID=gl${GL}rl${RL}pe${PROCS}
TEST_CASE_DIR=${NICAM_ROOT}/test/case/ICOMEX_JW
GRID_TEST_CASE_DIR=${TEST_CASE_DIR}/${GRID}
LOGDIR="${GRID_TEST_CASE_DIR}/nicam_logs/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOGDIR"

log "Changing to test case directory: ${GRID_TEST_CASE_DIR}"
cd "${GRID_TEST_CASE_DIR}"

PIDSTAT_LOG="pidstat.log"
IOSTAT_LOG="iostat.log"

log "Starting performance monitoring"
srun --overlap -v -l \
     --ntasks=1 --nodes=${SLURM_JOB_NUM_NODES} \
     --output="${LOGDIR}/%n.monitor.log" \
     ${GRID_TEST_CASE_DIR}/monitor_node.sh "$LOGDIR" 5 &

log "Running nhm_driver with mpirun (${PROCS} processes)..."
mpirun -np "${PROCS}" "${NICAM_ROOT}/nhm_driver"

log "Stopping resource monitoring..."
kill "${PIDSTAT_PID}" || true
kill "${IOSTAT_PID}" || true

log "Job completed successfully."
