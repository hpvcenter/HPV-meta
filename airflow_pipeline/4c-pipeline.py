import airflow

from datetime import datetime, timedelta
from airflow import DAG

from hopsworks_plugin.operators.hopsworks_operator import HopsworksLaunchOperator
# from hopsworks_plugin.operators.hopsworks_operator import HopsworksFeatureValidationResult
from hopsworks_plugin.sensors.hopsworks_sensor import HopsworksJobSuccessSensor

# Username in Hopsworks
# Click on Account from the top right drop-down menu
DAG_OWNER = 'dhananja'

## Project name this DAG belongs to
PROJECT_NAME = 'HPV-meta'

# Settings file for pipeline arguments
SETTINGS = "-s hdfs:///Projects/HPV-meta/Jupyter/HPV-meta/settings/settings_4C.yml"

"""
diamond or kraken as needed. 
"""
RUN_DIAMOND = False
RUN_KRAKEN = True

####################
## DAG definition ##
####################
delta = timedelta(minutes=-10)
now = datetime.now()

args = {
    'owner': DAG_OWNER,
    'depends_on_past': False,

    # DAG should have run 10 minutes before now
    # It will be automatically scheduled to run
    # when we upload the file in Hopsworks
    'start_date': now + delta,

    # Uncomment the following line if you want Airflow
    # to authenticate to Hopsworks using API key
    # instead of JWT
    #
    # NOTE: Edit only YOUR_API_KEY
    #

}

# Our DAG
dag = DAG(
    # Arbitrary identifier/name
    dag_id="4C_splitFastq_Kraken",
    default_args=args,

    # Run the DAG only one time
    # It can take Cron like expressions
    # E.x. run every 30 minutes: */30 * * * *
    schedule_interval="@once"
)

launch_splitFastq = HopsworksLaunchOperator(dag=dag,
                                            project_name=PROJECT_NAME,
                                            task_id="launch_splitFastq",
                                            job_name="splitFastq",
                                            job_arguments=SETTINGS,
                                            wait_for_completion=False)

wait_splitFastq = HopsworksJobSuccessSensor(dag=dag,
                                            project_name=PROJECT_NAME,
                                            task_id="wait_splitFastq",
                                            job_name="splitFastq")

launch_Trimming = HopsworksLaunchOperator(dag=dag,
                                          project_name=PROJECT_NAME,
                                          task_id="launch_Trimming",
                                          job_name="Trimming",
                                          job_arguments=SETTINGS,
                                          wait_for_completion=False)

wait_Trimming = HopsworksJobSuccessSensor(dag=dag,
                                          project_name=PROJECT_NAME,
                                          task_id="wait_Trimming",
                                          job_name="Trimming")

launch_NGM = HopsworksLaunchOperator(dag=dag,
                                     project_name=PROJECT_NAME,
                                     task_id="launch_NGM",
                                     job_name="NGM",
                                     job_arguments=SETTINGS,
                                     wait_for_completion=False)

wait_NGM = HopsworksJobSuccessSensor(dag=dag,
                                     project_name=PROJECT_NAME,
                                     task_id="wait_NGM",
                                     job_name="NGM")

launch_ConvertSam2BamUnmapped = HopsworksLaunchOperator(dag=dag,
                                                        project_name=PROJECT_NAME,
                                                        task_id="launch_ConvertSam2BamUnmapped",
                                                        job_name="ConvertSam2BamUnmapped",
                                                        job_arguments=SETTINGS,
                                                        wait_for_completion=False)

wait_ConvertSam2BamUnmapped = HopsworksJobSuccessSensor(dag=dag,
                                                        project_name=PROJECT_NAME,
                                                        task_id="wait_ConvertSam2BamUnmapped",
                                                        job_name="ConvertSam2BamUnmapped")

launch_Merge = HopsworksLaunchOperator(dag=dag,
                                       project_name=PROJECT_NAME,
                                       task_id="launch_Merge",
                                       job_name="Merge",
                                       job_arguments=SETTINGS,
                                       wait_for_completion=False)

wait_Merge = HopsworksJobSuccessSensor(dag=dag,
                                       project_name=PROJECT_NAME,
                                       task_id="wait_Merge",
                                       job_name="Merge")

launch_SortConvert = HopsworksLaunchOperator(dag=dag,
                                             project_name=PROJECT_NAME,
                                             task_id="launch_SortConvert",
                                             job_name="SortConvert",
                                             job_arguments=SETTINGS,
                                             wait_for_completion=False)

wait_SortConvert = HopsworksJobSuccessSensor(dag=dag,
                                             project_name=PROJECT_NAME,
                                             task_id="wait_SortConvert",
                                             job_name="SortConvert")



wait_splitFastq.set_upstream(launch_splitFastq)
launch_Trimming.set_upstream(wait_splitFastq)
wait_Trimming.set_upstream(launch_Trimming)
launch_NGM.set_upstream(wait_Trimming)
wait_NGM.set_upstream(launch_NGM)
launch_ConvertSam2BamUnmapped.set_upstream(wait_NGM)
wait_ConvertSam2BamUnmapped.set_upstream(launch_ConvertSam2BamUnmapped)
launch_Merge.set_upstream(wait_ConvertSam2BamUnmapped)
wait_Merge.set_upstream(launch_Merge)
launch_SortConvert.set_upstream(wait_Merge)
wait_SortConvert.set_upstream(launch_SortConvert)



if RUN_DIAMOND:
    launch_diamond = HopsworksLaunchOperator(dag=dag,
                                             project_name=PROJECT_NAME,
                                             task_id="launch_diamond",
                                             job_name="Diamond",
                                             job_arguments=SETTINGS,
                                             wait_for_completion=True)

    launch_diamond.set_upstream(wait_SortConvert)

if RUN_KRAKEN:
    launch_kraken = HopsworksLaunchOperator(dag=dag,
                                            project_name=PROJECT_NAME,
                                            task_id="launch_kraken",
                                            job_name="kraken",
                                            job_arguments=SETTINGS,
                                            wait_for_completion=True)


    launch_kraken.set_upstream(wait_SortConvert)
