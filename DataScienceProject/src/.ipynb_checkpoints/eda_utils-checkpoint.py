"""
Utility functions for credit scoring exploratory data analysis.

This module provides comprehensive functions for analyzing credit risk data,
including data quality assessment, statistical analysis, and visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import List, Tuple, Optional


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load credit scoring dataset from CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the credit scoring data
    """
    df = pd.read_csv(filepath)
    # Remove the unnamed index column if present
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    return df


def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comprehensive data quality report.
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with data quality metrics for each column
    """
    quality_report = pd.DataFrame({
        'Column': df.columns,
        'Data_Type': df.dtypes.values,
        'Missing_Count': df.isnull().sum().values,
        'Missing_Percentage': (df.isnull().sum() / len(df) * 100).values,
        'Unique_Values': df.nunique().values,
        'Sample_Values': [df[col].dropna().head(3).tolist() for col in df.columns]
    })
    return quality_report.sort_values('Missing_Percentage', ascending=False)


def basic_info(df: pd.DataFrame) -> None:
    """
    Display comprehensive information about the dataset.
    
    Args:
        df: Input DataFrame
    """
    print("=" * 80)
    print("DATASET OVERVIEW")
    print("=" * 80)
    print(f"Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")   # :.2f formats the number to 2 decimal places
    
    print("\n" + "=" * 80)
    print("DATA TYPES")
    print("=" * 80)
    print(df.dtypes)
    
    print("\n" + "=" * 80)
    print("MISSING VALUES SUMMARY")
    print("=" * 80)
    missing_df = pd.DataFrame({
        'Missing_Count': df.isnull().sum(),
        'Percentage': (df.isnull().sum() / len(df) * 100).round(2)
    })
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("No missing values found!")
    
    print("\n" + "=" * 80)
    print("NUMERICAL FEATURES STATISTICS")
    print("=" * 80)
    print(df.describe())
    
    print("\n" + "=" * 80)
    print("TARGET VARIABLE DISTRIBUTION")
    print("=" * 80)
    if 'SeriousDlqin2yrs' in df.columns:
        target_dist = df['SeriousDlqin2yrs'].value_counts()
        target_pct = df['SeriousDlqin2yrs'].value_counts(normalize=True) * 100
        print(f"Class 0 (No Default): {target_dist[0]:,} ({target_pct[0]:.2f}%)")
        print(f"Class 1 (Default): {target_dist[1]:,} ({target_pct[1]:.2f}%)")
        print(f"Class Imbalance Ratio: 1:{target_dist[0]/target_dist[1]:.2f}")


def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.Series:
    """
    Detect outliers in a numerical column using IQR or Z-score method.
    
    Args:
        df: Input DataFrame
        column: Column name to check for outliers
        method: 'iqr' or 'zscore'
        
    Returns:
        Boolean Series indicating outliers
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (df[column] < lower_bound) | (df[column] > upper_bound)
    elif method == 'zscore':
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        return z_scores > 3
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")


def plot_distribution(df: pd.DataFrame, column: str, title: Optional[str] = None, 
                     hue: Optional[str] = None, bins: int = 50) -> plt.Figure:
    """
    Plot distribution of a numerical column with enhanced visualizations.
    
    Args:
        df: Input DataFrame
        column: Column name to plot
        title: Custom title for the plot
        hue: Column name for color grouping
        bins: Number of bins for histogram
        
    Returns:
        Matplotlib figure object
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histogram with KDE
    if hue:
        for label in df[hue].unique():
            subset = df[df[hue] == label][column].dropna()
            axes[0].hist(subset, bins=bins, alpha=0.6, label=f'{hue}={label}', density=True)
        axes[0].legend()
    else:
        axes[0].hist(df[column].dropna(), bins=bins, alpha=0.7, edgecolor='black')
        df[column].dropna().plot(kind='kde', ax=axes[0], secondary_y=True, color='red', linewidth=2)
    
    axes[0].set_title(title or f'Distribution of {column}')
    axes[0].set_xlabel(column)
    axes[0].set_ylabel('Frequency')
    axes[0].grid(alpha=0.3)
    
    # Box plot
    if hue:
        df.boxplot(column=column, by=hue, ax=axes[1])
        axes[1].set_title(f'{column} by {hue}')
    else:
        axes[1].boxplot(df[column].dropna())
        axes[1].set_title(f'Box Plot of {column}')
    axes[1].set_ylabel(column)
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_categorical(df: pd.DataFrame, column: str, title: Optional[str] = None, 
                     top_n: Optional[int] = None) -> plt.Figure:
    """
    Plot count and percentage of categorical column.
    
    Args:
        df: Input DataFrame
        column: Column name to plot
        title: Custom title for the plot
        top_n: Show only top N categories
        
    Returns:
        Matplotlib figure object
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    value_counts = df[column].value_counts()
    if top_n:
        value_counts = value_counts.head(top_n)
    
    # Count plot
    value_counts.plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
    axes[0].set_title(title or f'Count of {column}')
    axes[0].set_xlabel(column)
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', alpha=0.3)
    
    # Percentage plot
    value_pct = (value_counts / len(df) * 100)
    value_pct.plot(kind='bar', ax=axes[1], color='coral', edgecolor='black')
    axes[1].set_title(f'Percentage Distribution of {column}')
    axes[1].set_xlabel(column)
    axes[1].set_ylabel('Percentage (%)')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig


def correlation_analysis(df: pd.DataFrame, numerical_cols: List[str], 
                        method: str = 'pearson') -> Tuple[plt.Figure, pd.DataFrame]:
    """
    Generate correlation matrix with enhanced visualization.
    
    Args:
        df: Input DataFrame
        numerical_cols: List of numerical column names
        method: Correlation method ('pearson', 'spearman', 'kendall')
        
    Returns:
        Tuple of (figure, correlation DataFrame)
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    correlation = df[numerical_cols].corr(method=method)
    
    # Create mask for upper triangle
    mask = np.triu(np.ones_like(correlation, dtype=bool))
    
    sns.heatmap(correlation, mask=mask, annot=True, fmt='.3f', 
                cmap='coolwarm', center=0, square=True, 
                linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    
    ax.set_title(f'Correlation Matrix ({method.capitalize()})', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return fig, correlation


def plot_target_relationship(df: pd.DataFrame, feature: str, target: str = 'SeriousDlqin2yrs') -> plt.Figure:
    """
    Visualize relationship between a feature and the target variable.
    
    Args:
        df: Input DataFrame
        feature: Feature column name
        target: Target column name
        
    Returns:
        Matplotlib figure object
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Distribution by target class
    for label in sorted(df[target].unique()):
        subset = df[df[target] == label][feature].dropna()
        axes[0].hist(subset, bins=30, alpha=0.6, label=f'{target}={label}', density=True)
    
    axes[0].set_title(f'{feature} Distribution by {target}')
    axes[0].set_xlabel(feature)
    axes[0].set_ylabel('Density')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Box plot by target class
    df.boxplot(column=feature, by=target, ax=axes[1])
    axes[1].set_title(f'{feature} by {target}')
    axes[1].set_xlabel(target)
    axes[1].set_ylabel(feature)
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    return fig


def calculate_woe_iv(df: pd.DataFrame, feature: str, target: str = 'SeriousDlqin2yrs', 
                     bins: int = 10) -> pd.DataFrame:
    """
    Calculate Weight of Evidence (WoE) and Information Value (IV) for a feature.
    
    Args:
        df: Input DataFrame
        feature: Feature column name
        target: Target column name
        bins: Number of bins for continuous variables
        
    Returns:
        DataFrame with WoE and IV calculations
    """
    # Create bins for continuous variables
    df_temp = df[[feature, target]].dropna().copy()
    
    if df_temp[feature].dtype in ['float64', 'int64'] and df_temp[feature].nunique() > bins:
        df_temp['binned'] = pd.qcut(df_temp[feature], q=bins, duplicates='drop')
    else:
        df_temp['binned'] = df_temp[feature]
    
    # Calculate WoE and IV
    grouped = df_temp.groupby('binned')[target].agg(['sum', 'count'])
    grouped.columns = ['events', 'total']
    grouped['non_events'] = grouped['total'] - grouped['events']
    
    total_events = grouped['events'].sum()
    total_non_events = grouped['non_events'].sum()
    
    grouped['event_rate'] = grouped['events'] / total_events
    grouped['non_event_rate'] = grouped['non_events'] / total_non_events
    
    # Avoid division by zero
    grouped['event_rate'] = grouped['event_rate'].replace(0, 0.0001)
    grouped['non_event_rate'] = grouped['non_event_rate'].replace(0, 0.0001)
    
    grouped['WoE'] = np.log(grouped['non_event_rate'] / grouped['event_rate'])
    grouped['IV'] = (grouped['non_event_rate'] - grouped['event_rate']) * grouped['WoE']
    
    total_iv = grouped['IV'].sum()
    
    print(f"\nInformation Value for {feature}: {total_iv:.4f}")
    print("IV Interpretation:")
    if total_iv < 0.02:
        print("  - Not useful for prediction")
    elif total_iv < 0.1:
        print("  - Weak predictive power")
    elif total_iv < 0.3:
        print("  - Medium predictive power")
    elif total_iv < 0.5:
        print("  - Strong predictive power")
    else:
        print("  - Suspicious (too good to be true, check for data leakage)")
    
    return grouped


def impute_missing_values(df: pd.DataFrame, method: str = 'mean', 
                         numerical_cols: Optional[List[str]] = None,
                         column_methods: Optional[dict] = None) -> pd.DataFrame:
    """
    Impute missing values in numerical columns.
    
    Args:
        df: Input DataFrame
        method: Default imputation method ('mean', 'median', 'mode')
        numerical_cols: List of numerical columns to impute. If None, auto-detect.
        column_methods: Optional dict mapping column names to specific methods.
                       e.g., {'MonthlyIncome': 'median', 'NumberOfDependents': 'mode'}
        
    Returns:
        DataFrame with imputed values
    """
    df_imputed = df.copy()
    
    # Auto-detect numerical columns if not provided
    if numerical_cols is None:
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Initialize column_methods if not provided
    if column_methods is None:
        column_methods = {}
    
    imputation_summary = []
    
    for col in numerical_cols:
        missing_count = df_imputed[col].isnull().sum()
        
        if missing_count > 0:
            # Use column-specific method if provided, otherwise use default method
            impute_method = column_methods.get(col, method)
            
            if impute_method == 'mean':
                fill_value = df_imputed[col].mean()
            elif impute_method == 'median':
                fill_value = df_imputed[col].median()
            elif impute_method == 'mode':
                fill_value = df_imputed[col].mode()[0]
            else:
                raise ValueError("Method must be 'mean', 'median', or 'mode'")
            
            # Use fillna without inplace to ensure it works on the copy
            df_imputed[col] = df_imputed[col].fillna(fill_value)
            
            imputation_summary.append({
                'Column': col,
                'Missing_Count': missing_count,
                'Imputation_Method': impute_method,
                'Fill_Value': round(fill_value, 4)
            })
    
    if imputation_summary:
        print(f"\n{'='*80}")
        print(f"MISSING VALUE IMPUTATION SUMMARY")
        print(f"{'='*80}")
        summary_df = pd.DataFrame(imputation_summary)
        for _, row in summary_df.iterrows():
            print(f"  {row['Column']:<45} Missing: {row['Missing_Count']:>6,}  →  {row['Imputation_Method']:>6} → {row['Fill_Value']:>10.4f}")
        print(f"{'='*80}")
        print(f"✓ Total columns imputed: {len(imputation_summary)}")
        print(f"✓ Total missing values filled: {sum([x['Missing_Count'] for x in imputation_summary]):,}")
    else:
        print("\n✓ No missing values found. No imputation needed.")
    
    return df_imputed


def statistical_test(df: pd.DataFrame, feature: str, target: str = 'SeriousDlqin2yrs') -> dict:
    """
    Perform statistical tests to assess feature significance.
    
    Args:
        df: Input DataFrame
        feature: Feature column name
        target: Target column name
        
    Returns:
        Dictionary with test results
    """
    df_clean = df[[feature, target]].dropna()
    
    group_0 = df_clean[df_clean[target] == 0][feature]
    group_1 = df_clean[df_clean[target] == 1][feature]
    
    # Perform t-test
    t_stat, p_value = stats.ttest_ind(group_0, group_1)
    
    # Perform Mann-Whitney U test (non-parametric)
    u_stat, p_value_mw = stats.mannwhitneyu(group_0, group_1)
    
    results = {
        'feature': feature,
        't_statistic': t_stat,
        'p_value_ttest': p_value,
        'u_statistic': u_stat,
        'p_value_mannwhitney': p_value_mw,
        'significant_at_0.05': p_value < 0.05,
        'mean_class_0': group_0.mean(),
        'mean_class_1': group_1.mean(),
        'median_class_0': group_0.median(),
        'median_class_1': group_1.median()
    }
    
    return results
