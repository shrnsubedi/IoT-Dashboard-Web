# from django.db import migrations


# class Migration(migrations.Migration):

#     dependencies = [
#         ("sensor", "0001_initial"),
#     ]

#     operations = [
#         migrations.RunSQL("SELECT create_hypertable('sensor_sensorreading', 'time');"),
#         migrations.RunSQL(
#             "ALTER TABLE sensor_sensorreading SET (timescaledb.compress, timescaledb.compress_segmentby = 'sensor_id');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_compression_policy('sensor_sensorreading', INTERVAL '7 days');"
#         ),
#     ]