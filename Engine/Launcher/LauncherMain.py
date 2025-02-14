import json
import os
import time

from Engine.DataObjects import Event
from Engine.Launcher.FileSegregator import FileSegregator
from Engine.Launcher.TaskPerformer import TaskPerformer
from Runner.Monitor.PubSub import Publisher


def main():
    try:
        # Initialize the monitor
        monitor = Publisher()

        # System initialization countdown
        for i in range(5):
            print(f"System initializing in {5 - i}...")
            time.sleep(1)

        monitor.publish(objective="Imported all the modules..", module="RUNNER")

        # Get the folder path for temporary storage
        folder_path = os.path.join(os.path.dirname(__file__), 'TempFileStorage\\')
        print(folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Initialize event
        event = Event.EventData(event_id=1234, monitor=monitor)

        # Segregate files
        file_segregator = FileSegregator(folder_path, event, monitor)
        if not file_segregator.segregate_files():
            return {"error": "No files found to process"}

        # Perform analysis tasks
        task_performer = TaskPerformer(event, monitor)
        start_time = time.time()
        json_vector_response, json_llm_response = task_performer.perform_tasks()
        end_time = time.time()
        execution_time = end_time - start_time
        monitor.publish(objective="Fetched Image analysis...", module="LOG (ImageProcessor)")

        if not json_vector_response or not json_llm_response:
            return {"error": "Analysis failed to produce results"}

        # Create serial ID to filename mapping
        serial_name_mapping = {}
        for item in event.data_items:
            if item.data_type == "image":
                path = item.image_path
            elif item.data_type == "audio":
                path = item.audio_path
            elif item.data_type == "video":
                path = item.video_path
            else:
                continue

            file_name = os.path.basename(path)
            serial_id = f"{event.event_id}.{item.serial_id}"
            serial_name_mapping[serial_id] = file_name

        # Process and combine results
        processed_results = process_datasets(json_vector_response, json_llm_response, serial_name_mapping)

        # Return empty result if no processing occurred
        if not processed_results:
            return {"error": "No results were processed"}

        return processed_results

    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


def process_datasets(dataset1, dataset2, id_to_filename):
    """Process and combine the vector and LLM analysis results."""
    try:
        results = []

        if not dataset1 or not dataset2:
            return []

        for entry1 in dataset1:
            serial_id = entry1.get('serial_id')
            if not serial_id:
                continue

            llm_scores = entry1.get('score', {})

            # Find corresponding vector analysis entry
            entry2 = next((item for item in dataset2 if item.get('serial_id') == serial_id), None)
            vector_scores = entry2.get('score', {}) if entry2 else {}

            # Get filename from mapping
            filename = id_to_filename.get(serial_id, "unknown")

            if vector_scores:
                # Combine scores
                combined_scores = {}
                all_keys = set(llm_scores.keys()) | set(vector_scores.keys())

                for key in all_keys:
                    llm_value = llm_scores.get(key, 0)
                    vector_value = vector_scores.get(key, 0)
                    combined_scores[key] = (llm_value + vector_value) / 2

                # Calculate percentages for combined scores
                total_combined = sum(combined_scores.values()) or 1  # Avoid division by zero
                total_combined_score = {
                    key: (value / total_combined * 100)
                    for key, value in combined_scores.items()
                }

                # Prepare progress bar data
                progress_bars = {
                    key: min(100, max(0, score))  # Ensure values are between 0 and 100
                    for key, score in total_combined_score.items()
                }

                result = {
                    'filename': filename,
                    'llm_results': llm_scores,
                    'vector_results': vector_scores,
                    'combined_results': combined_scores,
                    'total_combined_score': total_combined_score,
                    'progress_bars': progress_bars
                }

                results.append(result)

        return results

    except Exception as e:
        print(f"Error processing datasets: {str(e)}")
        return []


if __name__ == "__main__":
    processed_result = main()
    print(json.dumps(processed_result, indent=4))
